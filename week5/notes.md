# Week 5
- Local File Disclosure (LFD)
  - Path Traversal
  - `"/app/files" + "../../etc/passwd"` => `/etc/passwd`
  - Removing `../` is quite common: `....//` => `../`, `..././` => `../`
  - Interesting filepaths:
    ```
    # Relative Paths
    ./
    ../

    # Webserver Stuff
    .htaccess
    /var/log/apache2/{access, error}.log
    /etc/apache2/apache2.conf
    /etc/nginx/nginx.conf

    # App Stuff
    .git
    app.py
    /home/${user}
    ~/.ssh/id_rsa

    # Linux Stuff
    /proc/self/{environ, cmdline}
    /etc/{passwd, shadow}
    /etc/resolv.conf
    ```
- Local File Inclusion (LFI)
  - Including as in `#include 'filename'` (C) or `include 'filename';` (PHP).
  - PHP also has `require 'filename';` but that will crash (500) if the file does not exist.
  - Useful if you can upload a file and view it - check if you can execute it on the server.
    - Either by including it or making the server think it is executable.
    - Often this is just based on file extension, i.e. visiting a .php file results in executing it.
    - This is how CSE's websites typically work: https://cgi.cse.unsw.edu.au/~z5361056/acc.py (on CSE's servers = not in scope BTW).
      - .py file with correct permissions so therefore it gets run.
- Server-Side Template Injection (SSTI)
  - `{{ "hello " + "world" }}` => `"hello world"`
  - e.g. `{{ "".__class__.__mro__[1].__subclasses__() }}`
    - MRO = method resolution order (i.e. we will check these classes in this order for the methods you try run)
      - ```python
          class A(object):
              def __repr__(self):
                  return 'A'

          class B_one(A):
              def __repr__(self):
                  return 'B1'

          class B_two(A):
              def __repr__(self):
                  return 'B2'

          class C(B_one):
              def __repr__(self):
                  return 'C'

          A.__subclasses__()  # => [__main__.B_one, __main__.B_two]
          C.__mro__  # => (__main__.C, __main__.B_one, __main__.A, object)
      ```
  - Useful Payloads
    - Check for the vuln: `{{7*6}}`
    - Output Flask config (often includes DB credentials or session secret keys): `{{config}}`
    - Read file: `{{'abc'.__class__.__base__.__subclasses__()[92].__subclasses__()[0].__subclasses__()[0]('/etc/passwd').read()}}`
      - You may have to mess with the indices a bit, e.g. on my Mac you want `111` instead of `92`.
    - Use code from a module (this example is also RCE): `{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}`
  - TBH stole MRO example and most of these payloads from https://kleiber.me/blog/2021/10/31/python-flask-jinja2-ssti-example/
- Server Side Request Forgery (SSRF)
  - Any time you can get a server to send a request (usually HTTP(S), but sometimes DNS, FTP or whatever else).
  - e.g. A website where you can upload an image by giving it a URL rather than actually uploading a file.
    - The website will (typically) download the file from the URL, so it must send a request to it, which may give you more information (especially if it's something more interesting than an image upload).
  - Maybe your URL gets info attached to it, e.g. the server sends a request to `http://yoursite.com/<insert_data_here>` or to `http://<insert_data_here>.yoursite.com`.
- Reverse Proxies/WAFs
  - Most WAFs you have to deal with in this course are very basic.
    - Mostly looking for characters or character combinations e.g. `;` and `--`.
    - Anything more complicated you'll usually get source code because it's otherwise just trial and error.
    - But don't trust this too much because idk what Andrew and Lachlan may have cooked up.
  - Real-world WAFs are a pain especially from large providers like Cloudflare, since you'll get banned from all the sites they proxy.
    - No way to see exactly what caused a block.
    - No way to know how many requests will get you banned.s