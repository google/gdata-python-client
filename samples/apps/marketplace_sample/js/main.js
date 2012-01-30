/* Copyright 2012 Google Inc. All Rights Reserved.
 *
 * @fileoverview This file first retrieves a list of all of the domain users
 * using an ajax call to the server. It also retrieves the user details for a
 * particular user again using an ajax call to the server.
 *
 * @author gunjansharma@google.com (Gunjan Sharma)
 */

$(document).ready(function() {
  $('#get_details').attr('disabled', true);
  $.ajax({
    type: 'POST',
    url: '../',
    dataType: 'text',
    error: function(request, textStatus) {
      alert('There was a problem loading data from the server.');
    },
    success: function(data, textStatus, request) {
      var users = jQuery.parseJSON(data);
      for (var i = 0; i < users.length; i++) {
        $('#users_list')
            .append($('<option></option>')
            .attr('value', i)
            .text(users[i]));
      }
      $('#get_details').attr('disabled', false);
    }
  });

  $('#get_details').click(function() {
    this.disabled = true;
    var username = $('#users_list option:selected').text();
    request_url = '../getdetails/' + username;
    $.ajax({
      type: 'GET',
      url: request_url,
      dataType: 'text',
      error: function(request, textStatus) {
        alert('There was a problem loading data from the server.');
        $('#get_details').attr('disabled', false);
      },
      success: function(data, textStatus, request) {
        var details = jQuery.parseJSON(data);
        var groups = details['groups'];
        var html = '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>';
        var groups_html =
            '<tr align="middle"><td><b>Name</b></td><td><b>ID</b></td><tr>';
        for (var i = 0; i < groups.length; i++) {
          group = groups[i];
          groups_html +=
              ('<tr><td>' + group['name'] +
               '</td><td>' + group['id'] +
               '</td></tr>');
        }
        groups_html = '<table align="center"  valign="center" border="1">' +
            groups_html + '</table>';

        var orgunit = details['orgunit'];
        var orgunit_html = '<b>Name:</b> ' + orgunit['name'] +
            '<br /><b>Path:</b> ' + orgunit['path'];

        var nicknames = details['nicknames'];
        nicknames_html = '';
        for (var i = 0; i < nicknames.length; i++) {
          nicknames_html += nicknames[i] + '<br />';
        }
        $('#details_table > tbody:last').append(
            html.format(groups_html, nicknames_html, orgunit_html));
        $('#get_details').attr('disabled', false);
      }
    });
  });
});

/**
 * Formats the string by replacing with the appropriate parameter.
 * The function replaces {i} with the i-th parameter. Here i is an integer.
 *
 * @return {String} the formated string.
 */
String.prototype.format = function() {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function(match, number) {
    return typeof args[number] != 'undefined' ? args[number] : match;
  });
};
