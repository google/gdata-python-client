// Copyright 2011, Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @author pti@google.com (Prashant Tiwari)
 */

/**
 * @fileoverview Contains JS methods for index.html 
 */

/**
 * Tracks the start index for the prev and next links
 */
var startIndex = 0;

/**
 * Creates the users' table on each page.
 * 
 * @param {Array}
 *          entries The user entries to be displayed on the table.
 * @param {Int}
 *          start The start index for items displayed in the table.
 * @param {Int}
 *          size The table size.
 * @returns The table html.
 */
buildUserTable = function(entries, start, size) {
  var html = [];
  html.push('<table>');
  html.push('<tr>', '<th width=\'10%\'>#</th>',
      '<th width=\'35%\'>Account Name</th>',
      '<th width=\'45%\'>User Name</th>',
      '<th width=\'10%\'>Is Admin</th>', '</tr>');
  for ( var i = 0; i < size; i++) {
    if (start + i < entries.length) {
      var className = ((i % 2) == 0) ? 'odd' : 'even';
      html.push('<tr class=\'' + className + '\'>');
      html.push('<td class=\'serialno\'>' + (start + i + 1) + '</td>');
      html.push('<td class=\'accountname\'>' + entries[start + i].username + '</td>');
      html.push('<td class=\'username\'>' + entries[start + i].given_name + ' '
          + entries[start + i].family_name + '</td>');
      if (entries[start + i].admin == 'true') {
        html.push('<td class=\'isadmin\'>Yes</td>');
      } else {
        html.push('<td></td>');
      }
      html.push('</tr>');
    }
  }
  html.push('</table>');
  return html.join('\n');
};

/**
 * Creates the back and forth navigator links.
 * 
 * @param {String}
 *          pagingElements The element that holds the paged content.
 * @param {Int}
 *          pagesize The page size.
 */
createNavigator = function(pagingElements, pagesize) {
  var paging_elements = pagingElements;
  var page_size = pagesize;

  return function() {
    var prev_link = document.getElementById('prev');
    prev_link.onclick = function() {
      if (startIndex - page_size >= 0) {
        startIndex = startIndex - page_size;
        var user_div = document.getElementById('users')
        user_div.innerHTML = buildUserTable(user_entries, startIndex,
            page_size);
      }
    };

    var next_link = document.getElementById('next');
    next_link.onclick = function() {
      if (startIndex == 0 && startIndex - page_size > 0) {
        startIndex = startIndex - page_size;
        var user_div = document.getElementById('users')
        user_div.innerHTML = buildUserTable(user_entries, startIndex,
            page_size);
      } else if (startIndex + page_size + 1 <= paging_elements.length) {
        startIndex = startIndex + page_size;
        var user_div = document.getElementById('users')
        user_div.innerHTML = buildUserTable(user_entries, startIndex,
            page_size);
      }
    };
  };
};

/**
 * Called when index.html loads
 */
function onload() {
  var user_div = document.getElementById('users')
  var entries_per_page = 25
  user_div.innerHTML = buildUserTable(user_entries, 0, entries_per_page);
  new createNavigator(user_entries, entries_per_page)();
}
