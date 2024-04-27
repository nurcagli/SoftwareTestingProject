from SoftwareTestingProject1.models import Model
from SoftwareTestingProject1.analysis import Analysis


class Database :
    def __init__(self):
        self.sampleClassAnalysis = Analysis()
    
    def save_db(self, classes):
        
        instance_list = []  # 
        classes_id = []  # Her sınıfın id değerlerini tutacak liste
        try:
            for clas in classes:
                if not clas:
                    continue
                for class_name, content in clas.items():
                    class_analyzed =  self.sampleClassAnalysis.class_analysis(content)

                    analysis_instance = Model( # analiz edilmiş sınıfı db'ye kaydetmek ıcın model nesnesı olusturmak.
                        ClassName=class_name,
                        JavaDocComments=class_analyzed['JavaDocComments'],
                        OtherComments=class_analyzed['OtherComments'],
                        CodeLines=class_analyzed['CodeLines'],
                        FunctionCount=class_analyzed['FunctionCount'],
                        CommentDeviation=class_analyzed['CommentDeviation'],
                        Loc=class_analyzed['Loc']
                    )
                    instance_list.append(analysis_instance)
        except Exception as e:
            print("Hata oluştu:", e)
            # Hata durumunda geri dönüş yapılabilir veya uygun bir hata işleme mekanizması uygulanabilir.
            return None

        Model.objects.bulk_create(instance_list) # verileri db'ye toplu kaydeder.
        classes_id = [instance.Id for instance in instance_list]    
        return classes_id
   
    def get_batch(self, classes_ıd): # verileri db den toplu almak için
        analysis_result = {}
        for class_ıd in classes_ıd:
            analysis_result[class_ıd] = Model.objects.filter(Id=class_ıd)
        
        return analysis_result
        
    