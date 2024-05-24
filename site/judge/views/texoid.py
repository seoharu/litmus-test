##########곽성대 제작, texoid에 대한 경로를 처리하기 위해 제작##########
from django.conf import settings
from django.http import HttpResponse,Http404
from django.shortcuts import render
from django.views.generic import View
import os
import json
import re

class TexoidView(View):
    def get(self, request, folder, file):
        tmp_path = os.path.dirname(settings.STATIC_ROOT)
        folder_path = os.path.join(tmp_path ,'static','texoid_cache', folder)
        file_path = os.path.join(folder_path,file)

        #파일 있는 경우에만 응답
        if os.path.exists(file_path):
            try:
                with open(os.path.join(folder_path,'meta')) as meta:
                    meta_data = json.load(meta)
                    if file == 'png':
                        with open(file_path,'rb') as f:
                            return HttpResponse(f.read(),content_type='image/png')
                    elif file == 'svg':
                        with open(file_path,'r') as f:
                            content = f.read()
                            #이미지 크기 변환
                            content = re.sub(r'width\s*=\s*["\'][^"\']*["\']', f'width="{meta_data["width"]}px"', content)
                            content = re.sub(r'height\s*=\s*["\'][^"\']*["\']', f'height="{meta_data["height"]}px"', content)
                            return HttpResponse(content, content_type='image/svg+xml')
            except Exception as e:
                #1.지원하지 않는 파일형식자 2.메타 데이터파일이 없는 경우 ==> 404에러
                raise Http404("Invalid File" ,e)
        
        #폴더 없는 경우 404 에러
        raise Http404("File does not exist",file_path)