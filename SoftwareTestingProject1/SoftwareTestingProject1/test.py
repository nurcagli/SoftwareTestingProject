from sqlite3 import IntegrityError
import unittest
from django.test import TestCase
import os
from SoftwareTestingProject1.models import Model
from SoftwareTestingProject1.gitClone import GitCloning
from SoftwareTestingProject1.database import Database
from SoftwareTestingProject1.analysis import Analysis
from SoftwareTestingProject1.regex import Regex
from git import Repo
import unittest
from parameterized import parameterized
from django.db import connection
from faker import Faker



class UnitTest(unittest.TestCase):

    def setUp(self):
        self.classAnlys= Analysis()
        self.regex=Regex()
        self.db = Database()
        self.clone = GitCloning()
        self.fake = Faker()
        self.test_repository_url = "https://github.com/mfadak/Odev1Ornek.git"
     
        self.clonedRepoPath = "test"
        self.clonedOtherPath ="zabbixTest"
        self.emptyPath ="emptyDir"
        self.classes = self.classAnlys.analyze_files(self.clonedRepoPath)
        self.class_ids = self.db.save_db(self.classes)
        
        self.fileAtmPath ="test\Ornek\src\pkt\Atm.java"
        with open(self.fileAtmPath, "r") as f:
            self.contentAtm = f.read()  # Dosya içeriğini oku
        
        self.fileMasterKartPath = "test\Ornek\src\pkt\MasterKart.java"
        with open(self.fileMasterKartPath, "r") as f:
            self.contentMasterKart = f.read()  # Dosya içeriğini oku
        
        self.fileProgramPath = "test\Ornek\src\pkt\Program.java"
        with open(self.fileProgramPath, "r") as f:
            self.contentProgram = f.read()  # Dosya içeriğini oku
         
       

       

    def test_clone_git_repository_with_None_url(self):
        # Geçersiz bir URL ile işlevi test etme
        repository_url = None
        # Hata oluşmasını beklediğimizde, assertRaisesRegex kullanarak hem hata türünü hem de hata mesajını kontrol edebiliriz.
        with self.assertRaisesRegex(ValueError, "Repository URL cannot be None"):
            self.clone.clone_git_repository(repository_url)


    def test_clone_git_repository_valid_url_1(self):   
        result = self.clone.clone_git_repository(self.test_repository_url) # Klonlanacak depo dizini olarak test_directory kullanılıyor
        #dönüş değerinin dizin oldugunu kontrol et. öyleyse clone işlemi başarılıdır.
        self.assertTrue(os.path.isdir(result))
    
    def test_clone_git_repository_valid_url_2(self):
        result = self.clone.clone_git_repository(self.test_repository_url) # Klonlanacak depo dizini olarak test_directory kullanılıyor
        # Klonlama için oluşturulan dizinin içerisindeki alt dizinlerin varlığını kontrol et
        has_subdirectories = False
        for _, dirs, _ in os.walk(result):
            if dirs:
                has_subdirectories = True
                break
        self.assertTrue(has_subdirectories)
        
    def test_clone_git_repository_invalid_url(self):
        invalid_url = "https://github.com/invalid_url"
        cloned_dir =  self.clone.clone_git_repository(invalid_url)
        assert cloned_dir is None

    #clone git repository methodu için yazıldı  
    def test_directory_already_exist(self):
        result = self.clone.clone_git_repository(self.test_repository_url) # Klonlanacak depo dizini olarak test_directory kullanılıyor
        # Klonlanan dizinin adında parantez içeren bir öğe var mı kontrol et
        # tekrarlı kayıt ise isminin yanında (count) belirtilir.
        has_suffix_in_target_dir = any('(' in item and ')' in item for item in os.listdir(os.path.dirname(result)))
        self.assertTrue(has_suffix_in_target_dir)

            
            
            
    def test_analyze_files(self):
        found_classes = self.classAnlys.analyze_files(self.clonedRepoPath)
        self.assertEqual(len(found_classes), 6)
        #Ornek1 için len

    @parameterized.expand([
        ( "clonedRepoPath" , 6),
        ( "clonedOtherPath", 5),
        # Diğer parametre setleri buraya eklenebilir
    ])
    def test_analyze_files_param(self, ParamPath, expected_length):
        path= getattr(self, ParamPath)
        found_classes = self.classAnlys.analyze_files(path)
        self.assertEqual(len(found_classes), expected_length)

    def test_analyze_files_empty_dir(self):
        found_classes = self.classAnlys.analyze_files(self.emptyPath)
        self.assertTrue(not found_classes)

  
    
    def test_total_lines(self):
        total= self.classAnlys.total_lines(self.contentAtm)
        self.assertEqual(total,28)
    
    @parameterized.expand([
        #("contentAtm", 2),
        ("contentAtm", 28),
        # Diğer test durumlarını buraya ekleyin
    ])
    def test_total_lines_param(self,content_name,count):
        content = getattr(self, content_name)
        total= self.classAnlys.total_lines(content)
        self.assertEqual(total,count)
    
    
    
    
    def test_count_code_lines(self):
        codeLine=self.classAnlys.count_code_lines(self.contentAtm)
        self.assertEqual(codeLine,11)
        
    def test_count_code_lines_2(self):
        codeLine=self.classAnlys.count_code_lines(self.contentMasterKart)
        self.assertEqual(17,codeLine)  
    
    @parameterized.expand([
        #("contentAtm", 2),
        ("contentMasterKart", 17),
        # Diğer test durumlarını buraya ekleyin
    ])
    def test_count_code_lines_param(self,content_name , count):
        content = getattr(self, content_name)
        codeLine=self.classAnlys.count_code_lines(content)
        self.assertEqual(count,codeLine)  
    
    
    
    
    def test_count_function(self):
        functionCount=self.regex.count_function(self.contentAtm)
        self.assertEqual(functionCount,2)
    
    @parameterized.expand([
        #("contentAtm", 2),
        ("contentMasterKart", 3),
        # Diğer test durumlarını buraya ekleyin
    ])
    def test_count_function_param(self, content_name, expected_count):
        #parametrelı sorgularda self.contentatm dogrudan kullanılamadıgı ıcın getattr kullanıldı.  
        content = getattr(self, content_name)
        function_count = self.regex.count_function(content)
        self.assertEqual(function_count, expected_count)
        
        
        
    
    def test_count_java_doc(self):
        countJavaDoc =self.regex.count_java_doc(self.contentAtm)
        self.assertEqual(countJavaDoc,10)
          
    #masterkart sınıfı için assert not reqex ( other comment  ve javadoc olmadıgını onayla)
    def test_count_java_doc_2(self):
        countJavaDoc= self.regex.count_java_doc( self.contentMasterKart)
        assert not countJavaDoc
    
    @parameterized.expand([
        ("contentMasterKart", 0),
        #("contentMasterKart", 3),
        # Diğer test durumlarını buraya ekleyin
    ])
    def test_count_java_doc_param(self,content_name,count):
        content = getattr(self, content_name)
        countJavaDoc =self.regex.count_java_doc(content)
        self.assertEqual(countJavaDoc,count) 
    
    
    
    
    
    def test_count_other_comment(self):
        countOtherComment = self.classAnlys.count_other_comment(self.contentAtm)
        self.assertEqual(countOtherComment,1)
    
    #masterkart sınıfı için assert not reqex ( other comment  ve javadoc olmadıgını onayla)
    def test_count_other_comment_2(self):
        countOtherComment = self.classAnlys.count_other_comment(self.contentMasterKart)
        assert not countOtherComment
        
    @parameterized.expand([
        ("contentAtm", 1),
        #("contentMasterKart", 3),
        # Diğer test durumlarını buraya ekleyin
    ])    
    def test_count_other_comment_param(self,content_name,count):
        content = getattr(self, content_name)
        countOtherComment = self.classAnlys.count_other_comment(content)
        self.assertEqual(countOtherComment,count)
    
    
    
    
    
    #single + multi line = other comments
    def test_single_line_comments(self):
        singleLineComment =self.regex.single_line_comments( self.contentAtm)
        self.assertEqual(singleLineComment ,1)

    @parameterized.expand([
        ("contentAtm", 1),
        #("contentMasterKart", 3),
        # Diğer test durumlarını buraya ekleyin
    ]) 
    def test_single_line_comments_param(self,content_name,countComments):
        content = getattr(self, content_name)
        singleLineComment =self.regex.single_line_comments( content)
        self.assertEqual(singleLineComment ,countComments )
    
    
    
    
    def test_multi_line_comments(self):
        multiLineComment =self.regex.multi_line_comments(self.contentAtm)
        self.assertEqual(multiLineComment ,0)
    
    @parameterized.expand([
        ("contentAtm", 0),
        #("contentMasterKart", 3),
        # Diğer test durumlarını buraya ekleyin
    ])  
    def test_multi_line_comments_param(self,content_name,countComments):
        content = getattr(self, content_name)
        multiLineComment =self.regex.multi_line_comments(content)
        self.assertEqual(multiLineComment ,countComments)   
    
         
         
         
         
    def test_calculate_comment_deviation(self):
        deviation = self.classAnlys.calculate_comment_deviation(10, 1, 11, 2)
        self.assertAlmostEqual(deviation,166.67,places =2)
         
    @parameterized.expand([
        (3, 4, 35, 6, -46.67),
        # Diğer test durumlarını buraya ekleyin
    ])
    def test_calculate_comment_deviation_param(self, javadoc_lines, other_comments, code_lines, functions, expected_deviation):
        deviation = self.classAnlys.calculate_comment_deviation(javadoc_lines, other_comments, code_lines, functions)
        self.assertAlmostEqual(deviation, expected_deviation, places=2)
        
        
        
        
        
    
    def test_extract_classes(self):
        classes = self.classAnlys.extract_classes(self.fileAtmPath)
        self.assertIn("Atm", classes, f"Atm sınıfı classes sözlüğünde bulunamadı.")
        
    def test_extract_classes_2(self):
        known_classes = ["MasterKart"]
        extracted_classes = self.classAnlys.extract_classes(self.fileMasterKartPath)
        self.assertTrue(all(key in known_classes for key in extracted_classes.keys()))
        # self.assertCountEqual(known_classes,extracted_classes)   
        
    @parameterized.expand([
        (["Program"], "fileProgramPath"),
        # Diğer test vakaları buraya eklenir
    ])
    def test_extract_classes_param(self, known_classes ,filePath):
        path = getattr(self, filePath)
        extracted_classes = self.classAnlys.extract_classes(path)
        self.assertTrue(all(key in known_classes for key in extracted_classes.keys()))
    
    
    
    
    def test_model_instance(self):
        model_instance = Model.objects.create(
            ClassName='ExampleClass',
            JavaDocComments=10,
            OtherComments=5,
            CodeLines=200,
            FunctionCount=15,
            CommentDeviation=0.75,
            Loc=250
        )
        self.assertIsInstance(model_instance, Model) 




#faker ile yazilan testler

    def test_extract_classes_with_fake_data(self):
         # Rastgele Java kodu oluştur
        java_code = """
        public class MyClass {{
            public static void main(String[] args) {{
                System.out.println("{}");
            }}
        }}
        """.format(self.fake.sentence())

        # Oluşturulan kodu .java dosyasına yaz
        with open("MyClass.java", "w") as file:
            file.write(java_code)
            
        classes = self.classAnlys.extract_classes("MyClass.java")
        self.assertIn("MyClass", classes, f"MyClass sınıfı classes sözlüğünde bulunamadı.")
            
       
        
    def test_class_analysis_with_fake_data(self):
        
        class_name = self.fake.word().capitalize() + self.fake.word().capitalize() + "Class"
        method_name1 = self.fake.word().lower() + self.fake.word().capitalize() + "()"
        method_name2 = self.fake.word().lower() + self.fake.word().capitalize() + "()"

        class_definition = f"""
        public class {class_name} {{

            // Bu sınıf, Faker kütüphanesi kullanılarak oluşturulmuştur.

            // {method_name1} fonksiyonu
            public void {method_name1} {{
                // Buraya {method_name1} fonksiyonunun işlevi gelebilir.
            }}

            // {method_name2} fonksiyonu
            public void {method_name2} {{
                // Buraya {method_name2} fonksiyonunun işlevi gelebilir.
            }}
        }}
        """
        classContent = self.classAnlys.class_analysis(class_definition)
        self.assertEqual (classContent["FunctionCount"] ,2 )
    
    
    
    def test_clone_git_with_fake_url(self):
        
        url = self.fake.url()
        returnResult = self.clone.clone_git_repository(url)
        self.assertIsNone (returnResult)
        
    
    
    def test_create_model_with_fake_data(self):
        # Faker nesnesi oluştur
        fake = Faker()

        # Faker ile rastgele veriler oluştur
        class_name = fake.word()
        java_doc_comments = fake.random_int(min=0, max=100)
        other_comments = fake.random_int(min=0, max=100)
        code_lines = fake.random_int(min=0, max=1000)
        function_count = fake.random_int(min=0, max=50)
        comment_deviation = fake.pydecimal(min_value=0, max_value=10, right_digits=2)
        loc = fake.random_int(min=0, max=1000)

        # Model nesnesi oluştur
        model_instance = Model(
            ClassName=class_name,
            JavaDocComments=java_doc_comments,
            OtherComments=other_comments,
            CodeLines=code_lines,
            FunctionCount=function_count,
            CommentDeviation=comment_deviation,
            Loc=loc
        )

        # Model nesnesini veritabanına kaydet
        model_instance.save()

        # Veritabanına kaydedilen nesneyi al
        saved_model = Model.objects.get(pk=model_instance.pk)

        # Kaydedilen nesnenin özelliklerini kontrol et
        self.assertEqual(saved_model.ClassName, class_name)
    
    
    def test_analyze_files_fake_path(self):
        random_file_path = self.fake.file_path()
        result = self.classAnlys.analyze_files(random_file_path)
        self.assertTrue(not result)
 
   
    
    # def tearDown(self):
    # #  Test sonrası geçici dizini temizle
    
    #     shutil.rmtree(self.test_directory)

    
    
class EntegrationTests(TestCase):
    
    def setUp(self):
        self.classAnlys= Analysis()
        self.regex=Regex()
        self.db = Database()

        self.test_repository_url = "https://github.com/mfadak/Odev1Ornek.git"
        
        self.clonedRepoPath = "test"
        self.classes = self.classAnlys.analyze_files(self.clonedRepoPath)
         # save_db , classes ıcındekı sınıf verilerini verıtabanına kaydeder ve kaydedılen sınıfların ıd lıstesını dondurur.
        self.class_ids = self.db.save_db(self.classes)
        
        
        self.fileAtmPath = "test\Ornek\src\pkt\Atm.java"
        with open(self.fileAtmPath, "r") as f:
            self.contentAtm = f.read()  # Dosya içeriğini oku
        
        self.fileMasterKartPath ="test\Ornek\src\pkt\MasterKart.java"
        with open(self.fileMasterKartPath, "r") as f:
            self.contentMasterKart = f.read()  # Dosya içeriğini oku

         # Test veritabanına bazı örnek sınıflar ekleyelim
        self.class1 = Model.objects.create(ClassName="Class1", JavaDocComments=5, OtherComments=3, CodeLines=100, FunctionCount=10, CommentDeviation=2, Loc=50)
        self.class2 = Model.objects.create(ClassName="Class2", JavaDocComments=8, OtherComments=4, CodeLines=150, FunctionCount=12, CommentDeviation=3, Loc=70)
        self.class3 = Model.objects.create(ClassName="Class3", JavaDocComments=3, OtherComments=2, CodeLines=80, FunctionCount=8, CommentDeviation=1, Loc=40)
        #saved_class_List =[Atm,Program,MasterKart,Kart  ]
    
    def test_save_db_integration(self):
        self.class_ids = self.db.save_db(self.classes)
        # Veritabanından kaydedilen veriyi alma
        analysis_result = {}
        for class_id in self.class_ids:
            analysis_result[class_id] = Model.objects.filter(Id=class_id) #ıd'ler ıle verıtabanı nesnelerı alınıyor.        
        #test , nesnenın varlıgının kontrolu
        savedİnstances = False
        for class_id, instances in analysis_result.items(): 
            if instances:
                savedİnstances = True
            else:
                savedİnstances =False
        self.assertTrue(savedİnstances)
    
    def test_save_db_no_error(self):    
        result = self.db.save_db(self.classes)
        self.assertIsNotNone(result)
    
    
    def test_get_batch (self):
        expected_result = {
           self.class_ids[0]: [Model(Id=self.class_ids[0],ClassName ="Atm",JavaDocComments = 10,OtherComments = 1, CodeLines= 11, FunctionCount=2, CommentDeviation =166.67, Loc = 28 )], # Model yerine uygun bir sınıf adı kullanılmalı
           self.class_ids[1]: [Model(Id=self.class_ids[1],ClassName = "Hesap", JavaDocComments = 3 , OtherComments = 4, CodeLines= 35 , FunctionCount=6, CommentDeviation = -46.67, Loc = 53)],
           self.class_ids[2]: [Model(Id=self.class_ids[2],ClassName = "Kart",JavaDocComments= 5 , OtherComments = 1, CodeLines= 17, FunctionCount=3,CommentDeviation = -5.88 , Loc = 33 )],
           self.class_ids[3]: [Model(Id=self.class_ids[3],ClassName = "MasterKart",JavaDocComments = 0 ,OtherComments = 0, CodeLines=17, FunctionCount=3, CommentDeviation = -100.00 , Loc = 22)],
           self.class_ids[4]: [Model(Id=self.class_ids[4],ClassName = "Program", JavaDocComments = 4, OtherComments = 6, CodeLines= 18, FunctionCount=1, CommentDeviation = 48.15,Loc = 33)],
           self.class_ids[5]: [Model(Id=self.class_ids[5],ClassName = "Week", JavaDocComments = 20, OtherComments = 2, CodeLines= 24, FunctionCount=6, CommentDeviation = 144.44,Loc = 64)]
        }
        
            #result
            # 904:<QuerySet [<Model: Model object (904)>]>
            # 905:<QuerySet [<Model: Model object (905)>]>
            # 906:<QuerySet [<Model: Model object (906)>]>
            # 907:<QuerySet [<Model: Model object (907)>]>
            # 908: <QuerySet [<Model: Model object (908)>]>

        result =self.db.get_batch(self.class_ids)
        transformed_result = {}
        for key, value in result.items():
            transformed_result[key] = list(value)

        self.assertEqual(transformed_result, expected_result)
        
    
    def test_get_batch_empty_classes_id(self):
        # Boş sınıf id listesiyle get_batch fonksiyonunu çağıralım
        analysis_result = self.db.get_batch([])
        # Boş bir sözlük döndürmesi beklenir
        self.assertEqual(len(analysis_result), 0)
    
    
    def test_correct_results_returned(self):
        # Veritabanındaki sınıf id'lerini bir listeye alalım
        class_ids = [self.class1.Id, self.class2.Id, self.class3.Id]

        # get_batch fonksiyonunu çağıralım
        analysis_result = self.db.get_batch(class_ids)

        # Her sınıfın doğru sonuçları içerdiğini kontrol edelim
        self.assertEqual(len(analysis_result), len(class_ids))
        for class_id in class_ids:
            self.assertIn(class_id, analysis_result)
    

            
if __name__ == "__main__":
    unittest.main()