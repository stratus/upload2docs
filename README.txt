 Copyright (C) 2010 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License


For more information on the upload2docs, please see the 
project on code.google.com's hosting service here: 
http://code.google.com/p/upload2docs/

Dependency Modules:

* gdata 2.0.7 or newer - http://code.google.com/p/gdata-python-client/

How to use it:

You will need a Google Apps Premier account. It won't work with your
regular Gmail or Google Apps Standard Edition. For more information
about this Premier feature, please read:

http://googleenterprise.blogspot.com/2010/01/store-and-share-files-in-cloud-with.html


Uploading <path> as <you@apps_premium_domain>:

  ./upload2docs --path <path> --username <you@apps_premier_domain.com>

Uploading <path> as <you@apps_premium_domain.com> also adding write 
permission to <friend@apps_premium_domain.com>:

  ./upload2docs --path <path> --username <you@apps_premier_domain.com> \
                --perm writer --type user \
                --value <friend@apps_premium_domain>

Uploading <path> as <you@apps_premium_domain.com> also adding reader 
permission to <group@apps_premium_domain.com>:

  ./upload2docs --path <path> --username <you@apps_premier_domain.com> \
                --perm reader --type group \
                --value <group@apps_premium_domain>

Uploading <path> as <you@apps_premium_domain.com> also adding writer 
permission to <apps_premium_domain.com>:

  ./upload2docs --path <path> --username <you@apps_premier_domain.com> \
                --perm writer --type domain \
                --value <apps_premium_domain.com>

