#encoding:utf-8
import httplib, mimetypes
import urlparse
import os
import sys
import datetime

version = 0.01
def post_multipart(host, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTPConnection(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    re=h.getresponse()
    
    return re.read()
    

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        #print "field:"+key
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        #print "file:"+key,filename
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def is_today(filename):
    today = datetime.datetime.now().strftime('%Y%m%d')
    if(filename.find(today) >= 0):
        return True
    else:
        return False
    #if(filename.)
    #print yesterday
 
def upload_logs(path,url):   
    os.chdir(path)
    
    upload_file_number=0;
    upload_file_number_suc=0;
    
    #压缩并计算有多少文件需要传
    for filename in os.listdir(path):
        if(not is_today(filename)):
            #print filename
            #check whethre need to gzip
            if(os.path.splitext(filename)[1]==".gz"):
                upload_file_name=filename
            else:
                os.system('gzip '+filename)
                upload_file_name=filename+".gz"
            
            if(os.path.exists(upload_file_name)):
                upload_file_number+=1;
            else:
                print filename+' gzip failed'
     
    print "number need to upload:%d" % upload_file_number;
    
    #开始上传
    for filename in os.listdir(path):
       if(os.path.splitext(filename)[1]==".gz"):
            print filename
            #########
            fields=[]
            filesize = '%d'%os.path.getsize(filename)
            print filesize
            fields.append(('filesize',filesize))
            
            #########
            file_content=open(filename).read()
            files=[]
            files.append(('upfile',filename,file_content))
            
            #########
            urlparts = urlparse.urlsplit(url)
            #print urlparts[0],urlparts[1], urlparts[2]
            try:
                resp = post_multipart(urlparts[1], urlparts[2], fields,files)
                print resp
                 #########
                if(resp.strip() == 'ok'):
                    upload_file_number_suc += 1
                    os.remove(filename)
                    
            except Exception, e:
                print e
            
           
            
    print "number really uploaded:%d" % upload_file_number_suc
    
def main():
    
    if(len(sys.argv)!=3):
        print 'arguments error! 1:dir 2:url'
        sys.exit()
    path = sys.argv[1]
    url = sys.argv[2]
    
    '''
    try:
        upload_logs(path,url)
    except Exception, e:
        print e
    '''
    upload_logs(path,url)
        
if __name__ == "__main__":
    main()






