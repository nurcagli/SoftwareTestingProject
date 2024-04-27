from django.http import HttpResponse
import os
import re
from SoftwareTestingProject1.regex import Regex

class Analysis:
    def __init__(self):
       self.regex =Regex()
        

    def analyze_files(self,directory):
        classes = []
        # Verilen dizindeki tüm dosyaları gez
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)  # Dosya yolu
                    class_dict = self.extract_classes(file_path)
                    if class_dict:
                        classes.append(class_dict) # dosyadaki siniflari dondurur
             
        return classes


    def extract_classes(self, file_path): # TRY CATCH EKLE, DOSYA ACARKEN HATA OLUSABILIR
        classes = {}
        with open(file_path, "r") as f:
            content = f.read()  # Dosya içeriğini oku
            # Dosyanın izinlerini belirle
            #os.chmod(file_path, 0o777)
          
            # Sınıf ifadesini bulmak için desen
            class_pattern = r'(((public|final|abstract|private|static|protected)\s+)?(class)\s+(\w+)(<.*>)?(\s+extends\s+\w+)?(<.*>)?(\s+implements\s+)?(.*)?(<.*>)?(\s*))\{'
            java_classes = re.finditer(class_pattern, content)
            for match in java_classes:
                class_name = match.group(5)  # Sınıf adı
                classes[class_name] = content
        return classes   
       
       

    def class_analysis(self, content):
        javadoc_lines = other_comments = code_lines = total_lines = functions= 0
       
        javadoc_lines += self.regex.count_java_doc(content)
        other_comments = self.count_other_comment(content)
        functions += self.regex.count_function(content)
        code_lines += self.count_code_lines(content)
        total_lines +=self.total_lines(content)
             
        #  yorum sapma yüzdesini hesapla
        if total_lines == 0:
            comment_deviation = float('inf')
        else:
            comment_deviation = self.calculate_comment_deviation(javadoc_lines, other_comments, code_lines, functions)
        
        # Analiz sonuçlarını döndür
        return {
            "JavaDocComments": javadoc_lines,
            "OtherComments": other_comments,
            "CodeLines": code_lines,
            "Loc": total_lines,
            "CommentDeviation": comment_deviation ,
            "FunctionCount" :functions
            # Diğer analiz sonuçlarını buraya ekle
        }

    def count_other_comment(self,content): 
        singleLineComments =self.regex.single_line_comments(content)
        multiLineComments = self.regex.multi_line_comments(content)
        total = multiLineComments + singleLineComments
        return total

    def count_code_lines(self, content):
        code_lines = 0
        in_comment = False

        for line in content.split('\n'):
            line = line.strip()

            if not line or line.startswith("//"):
                # Boş satır veya tek satırlık yorum satırı
                continue
            elif line.startswith("/**") or line.startswith("/*"):
                # JavaDoc yorumunun ya da Çoklu satırlı yorumunun başlangıcı
                in_comment = True
                if line.endswith("*/"):
                    # Çoklu satırlı yorum tek satırlık ise
                    in_comment = False
                continue
            elif in_comment and line.endswith("*/"):
                # Çoklu satırlı yorumun sonu 
                in_comment = False
                continue
            elif in_comment:
                # Çoklu satırlı yorumun devamı
                continue
            else:
                # Kod satırı
                code_lines += 1

        return code_lines

    def total_lines(self,content):
        total_lines=0
        #son satir kontrol
        lines = content.split('\n')
        last_line = lines[-1]
        if last_line.isspace() or last_line == "":
            total_lines -= 1
            
        for line in lines:      
            line = line.strip()
            total_lines += 1
        return total_lines
    
    def calculate_comment_deviation(self,javadoc_lines, other_comments, code_lines, functions):
        try:
            # YG'nin hesaplanması ve sıfıra bölünme durumunun ele alınması
            YG = ((javadoc_lines + other_comments) * 0.8) / functions

            # YH'nin hesaplanması ve sıfıra bölünme durumunun ele alınması
            YH = (code_lines / functions) * 0.3

            # Yorum Sapma Yüzdesinin hesaplanması ve sıfıra bölünme durumunun ele alınması
            comment_deviation = ((100 * YG) / YH) - 100

        except ZeroDivisionError:
            # Fonksiyon sayısı sıfır olduğunda sıfıra bölünme hatası alınır
            if (javadoc_lines + other_comments) == 0:
                # Hem Javadoc hem de diğer yorum satırları yoksa sonsuzluk
                return float('inf')
            else:
                # Sadece fonksiyon sayısı sıfır olduğunda sonsuzluk
                return 0

        return comment_deviation