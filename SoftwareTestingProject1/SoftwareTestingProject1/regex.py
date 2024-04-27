import re

class Regex:
    def __init__(self):
         pass

    def count_function(self,content):
        
        function_pattern =r'\b(?:public|private|protected|static|final|\s|implements|extends)+[\w<>\[\]]*\s+(\w+)\s*\([^)]*\)\s*(?:throws\s+\w+\s*)?\{'
        functions = re.findall(function_pattern,content , re.DOTALL)    
        return len(functions)
    
    

    def count_java_doc(self,content):
        
        javadoc_pattern = r'/\*\*.*?\*/'  # Javadoc yorumlarını tanımlayan regex deseni
        javadoc_comments = re.finditer(javadoc_pattern, content, re.DOTALL)
        total_comment_lines = 0

        for match in javadoc_comments:
            javadoc_start_index = match.start()
            javadoc_end_index = match.end()

            # Javadoc yorumunu al
            javadoc_content = content[javadoc_start_index:javadoc_end_index]

            # Yorum satırlarını say
            comment_lines = javadoc_content.split('\n') 
            comment_lines = [line.strip() for line in comment_lines if not line.strip().startswith("/**") and not line.strip().startswith("*/")]
            total_comment_lines += len(comment_lines)

        return total_comment_lines
    
    
    def single_line_comments(self,content):
        
        #pattern = r'(//.*$|/\*.*?\*/)'
        pattern = r"\/\/[^\n]*|\/\*[\s\S]*?\*\/"
        comments = re.finditer(pattern, content, re.DOTALL)
        total_count = 0

        for match in comments:
            
            # Eşleşmenin metnini al
            comment = match.group(0)
            
            # Eğer yorum satırı tek satırlık bir yorumsa ve başlangıcı "//" ise,
            # bu bir normal tek satırlık yorumdur.   
            lines = comment.split('\n') 
            single_comment_lines = [line.strip() for line in lines if line.strip().startswith("//") ]
            #single_comment_lines = [line.strip() for line in lines]
            total_count += len(single_comment_lines)
        return total_count
    
    
    def multi_line_comments(self,content):
        pattern = r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
        comments = re.finditer(pattern,content,re.DOTALL)
        total = 0
        
        for match in comments:
            comment = match.group(0)
            
            if comment.startswith("/**"):
                continue
            
            start_index = match.start()
            end_index = match.end()  
            content = content[start_index:end_index]
    
            comment_lines = content.split('\n') 
            comment_lines = [line.strip() for line in comment_lines if not line.strip().startswith("/*") and not line.strip().startswith("*/") ]
            total += len(comment_lines)
        return total
        
    
