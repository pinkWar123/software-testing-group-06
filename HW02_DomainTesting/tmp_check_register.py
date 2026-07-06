import json, urllib.request, urllib.error

cases = [
    ('TC-FR01-01','Nguyen Van A','fr01-01@test.com','Abcdef1!'),
    ('TC-FR01-02','', 'fr01-02@test.com','Abcdef1!'),
    ('TC-FR01-03','Le Thi B','invalid-email','Abcdef1!'),
    ('TC-FR01-04','Le Thi B','', 'Abcdef1!'),
    ('TC-FR01-05','Tran Van C','fr01-dup-base@test.com','Abcdef1!'),
    ('TC-FR01-06','Tran Van C','fr01-dup-base@test.com','Abcdef1!'),
    ('TC-FR01-07','Tran Van C','fr01-07@test.com','abcdef1!'),
    ('TC-FR01-08','Tran Van C','fr01-08@test.com','ABCDEF1!'),
    ('TC-FR01-09','Tran Van C','fr01-09@test.com','Abcdef!'),
    ('TC-FR01-10','Tran Van C','fr01-10@test.com','Abcdef1'),
    ('TC-FR01-11','Tran Van C','fr01-11@test.com','Abcde1!'),
    ('TC-FR01-12','Tran Van C','fr01-12@test.com',''),
    ('TC-FR01-13','Tran Van C','fr01-13@test.com','Abcdef1!'),
    ('TC-FR01-14','Tran Van C','fr01-14@test.com','Abcdef1!'),
    ('TC-FR01-15','Pham Thi D','fr01-15@test.com','Abcde12!'),
    ('TC-FR01-BVA-01','Nguyen Van A','bva1@test.com','Abcde1!'),
    ('TC-FR01-BVA-02','Nguyen Van A','bva2@test.com','Abcdef1!'),
    ('TC-FR01-BVA-03','Nguyen Van A','bva3@test.com','Abcdefg1!'),
    ('TC-FR01-BVA-04','Nguyen Van A','bva4@test.com','Abcdef1#')
]

for tc, name, email, password in cases:
    data = json.dumps({'name': name, 'email': email, 'password': password}).encode()
    req = urllib.request.Request('http://localhost:3000/api/register', data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode('utf-8', errors='replace')
            print(f"{tc}|status=200|body={body}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        print(f"{tc}|status={e.code}|body={body}")
    except Exception as e:
        print(f"{tc}|error={e}")
