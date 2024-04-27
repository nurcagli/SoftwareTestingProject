from django.shortcuts import render
from django.http import HttpResponse
from SoftwareTestingProject1.analysis import Analysis
from SoftwareTestingProject1.gitClone import GitCloning
from SoftwareTestingProject1.models import Model
from SoftwareTestingProject1.database import Database

import os
import shutil



def index(request): #view bir istek aldiginda calisir.
    if request.method == "POST":
        repository_url = request.POST.get('repo_url')

        classAnalysis= Analysis()
        db= Database()
        
        # GitHub deposunu klonla
        gitclone = GitCloning()
        clonedRepoPath = gitclone.clone_git_repository(repository_url)

        if clonedRepoPath is not None:
            classes = classAnalysis.analyze_files(clonedRepoPath) # butun class ıcerıklerı burada bulunur
            if classes:    
                classes_ıd= db.save_db(classes)

                # VERİTABANINDAN ANALİZ SONUCUNU AL
                analysis_result = db.get_batch(classes_ıd) #yenı eklenen sınıf objelerını dondurecek
                
                gitclone.kill_processes_using_directory(clonedRepoPath)

                # Sonuçları sonuc.html şablonuna gönder
                return render(request, 'sonuc.html', {'analysis_result': analysis_result})
            else:
                return render(request, 'sonuc.html')
        else:
            results = Model.objects.all()
            return render (request, 'index.html', {'results':results })


    elif request.method == "GET":
        results = Model.objects.all()
        return render (request, 'index.html', {'results':results })
    





