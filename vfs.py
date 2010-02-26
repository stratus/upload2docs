#!/usr/bin/env python
#
# Copyright 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""A vfs module to Google Docs."""

__author__ = 'stratus@google.com (Gustavo Franco)'

import logging
import mimetypes
import os
import gdata.acl.data
import gdata.docs.client

CONTENT_TYPE_FALLBACK = 'application/octet-stream'


class VFS(object):
  """A Virtual File System object to Google Docs."""

  def __init__(self, email, password, source=None, additional_headers=None,
               log_level=None, http_debug=None):
    self.gd_client = gdata.docs.client.DocsClient()
    self.gd_client.email = email
    self.gd_client.password = password
    if http_debug:
      self.gd_client.http_client.debug = True
    if not source:
      self.gd_client.source = 'google-upload2docsvfs'
    else:
      self.gd_client.source = source
    if not additional_headers:
      self.gd_client.additional_headers = {'GData-Version': 3.0}
    else:
      self.gd_client.additional_headers = additional_headers
    self.logger = logging.getLogger('vfs')
    if log_level:
      self.logger.setLevel(log_level)
    self.logger.debug('email is set to %s.', email)
    self.logger.debug('password is set to %s.', password)
    self.logger.debug('source is set to %s.', self.gd_client.source)
    self.logger.debug('additional_headers is set to %s.',
                      self.gd_client.additional_headers)
    self.gd_client.ClientLogin(self.gd_client.email, self.gd_client.password,
                               self.gd_client.source)

  def Copy(self, path, title=None, target=None):
    """Copy a file to Google Docs.

    Args:
      path: Path to file that will be uploaded to Google Docs.
      title: (optional) Title, file name will be used if not given.
      target: (optional) (sub)directory gdata.data.DocsEntry if not / .

    Returns:
      gdata.data.DocsEntry of uploaded file.
    """
    if not os.path.isfile(path):
      self.logger.error('%s is not a valid file name.', path)
      return

    if title is None:
      title = os.path.basename(path)

    content_type = self.__ContentType(path)
    self.logger.debug('Uploading %s (%s, %s bytes).', path, content_type,
                      os.path.getsize(path))
    entry = None
    if target is None:
      uri = '%s?convert=false' % gdata.docs.client.DOCLIST_FEED_URI
      entry = self.gd_client.Upload(path, title, content_type=content_type,
                                    folder_or_uri=uri)
    else:
      resource_id = target.resource_id.text
      uri = '%s%s/contents?convert=false' % (gdata.docs.client.DOCLIST_FEED_URI,
                                             resource_id)
      entry = self.gd_client.Upload(path, title, content_type=content_type,
                                    folder_or_uri=uri)

    if entry is not None:
      self.logger.debug('%s is using %s bytes and is at: %s',
                        path, entry.quota_bytes_used.text,
                        entry.GetAlternateLink().href)
    else:
      self.logger.error('Upload error while trying to send %s.', path)
    return entry

  def Mkdir(self, directory, target=None):
    """Make a directory in Google Docs.

    Args:
      directory: Directory name to be created in Google Docs.
      target: (optional) (sub)directory gdata.data.DocsEntry if not / .

    Returns:
      gdata.data.DocsEntry of directory created.
    """
    dir_entry = None
    if target is None:
      self.logger.debug('Trying to make %s directory in Google Docs.',
                        directory)
      dir_entry = self.gd_client.Create(gdata.docs.data.FOLDER_LABEL,
                                        directory)
      self.logger.debug('Directory %s was created.', dir_entry.title.text)
    else:
      self.logger.debug('Trying to make %s subdirectory into %s directory.',
                        directory, target.title.text)
      dir_entry = self.gd_client.Create(gdata.docs.data.FOLDER_LABEL,
                                        directory, folder_or_id=target)
      self.logger.debug('Subdirectory %s created into %s.',
                        dir_entry.title.text, target.title.text)
    return dir_entry

  def Chmod(self, sharetype, sharewith, shareperm, target,
            add_or_remove='add'):
    """Add or remove permissions to a directory in Google Docs.

    Args:
      sharetype: user, domain or group.
      sharewith: a given user, a domain or a group that will get permission.
      shareperm: The permission itself that must be reader, writer or owner.
      target: gdata.docs.DocsEntry to add permission to.
      add_or_remove: (optional) Defaults to add permissions.

    Returns:
      ACL feed with directory properties.
    """
    if add_or_remove is not 'add':
      self.logger.critical('Just add permission has been implemented yet.')
    scope = gdata.acl.data.AclScope(value=sharewith, type=sharetype)
    role = gdata.acl.data.AclRole(value=shareperm)
    acl_entry = gdata.docs.data.Acl(scope=scope, role=role)
    self.logger.debug('Giving %s %s %s privileges.', sharetype, sharewith,
                      shareperm)
    new_acl = self.gd_client.Post(acl_entry, target.GetAclFeedLink().href)
    if new_acl.scope.type:
      self.logger.debug('Giving %s %s %s privileges.', new_acl.scope.type,
                        new_acl.scope.value, new_acl.role.value)
    return new_acl

  def __ContentType(self, path):
    """Lookup file content type.

    Args:
      path: Path to file that will be looked up for its content type.

    Returns:
      File content type.
    """
    mimetypes.init()
    file_extension = path[path.rfind('.'):]
    if not file_extension in mimetypes.types_map:
      self.logger.debug('Could not find mimetype for %s extension %s.', path,
                        file_extension)
      self.logger.debug('Falling back to %s.', CONTENT_TYPE_FALLBACK)
      content_type = CONTENT_TYPE_FALLBACK
    else:
      content_type = mimetypes.types_map[file_extension]
    return content_type
