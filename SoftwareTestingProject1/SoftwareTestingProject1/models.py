from django.db import models


class Model(models.Model):
    Id = models.AutoField(primary_key=True)
    ClassName = models.CharField(max_length=50)
    JavaDocComments =models.IntegerField ()
    OtherComments =models.IntegerField ()
    CodeLines =models.IntegerField()
    FunctionCount = models.IntegerField()
    CommentDeviation = models.DecimalField(max_digits=6, decimal_places=2)
    Loc = models.IntegerField()


       