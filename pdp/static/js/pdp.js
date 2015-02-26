// possible js tools for the project

// common variables
var v_remoteUser = '';
var v_xsrf = '';
var v_etag = '';
var iam_loadErrorMessage = "Operation failed. You may need to reload the page to reauthenticate";

// Trim leading and following spaces from a string
String.prototype.trim = function () {
   return this.replace(/^\s*|\s*$/g,"");
}

/*
 * show/hide a dialog
 */

// show: id is dialog element id
function iam_showTheDialog(id) {
   var d = $('#'+id);
   if (d==null) {
      console.log('dialog ' + id + ' not found');
      return;
   }
   d.dialog({
      modal: true,
      show: 'fade',
      hide: 'fade',
      dialogClass: 'dialogStyle',
   });
}

// hide
function iam_hideTheDialog(id) {
   var d = $('#'+id);
   if (d==null) {
      console.log('dialog ' + id + ' not found');
      return;
   }
   d.dialog('close');
}

// dialogs without predefined elements

// show a formatted message
function iam_showTheMessage(msg, title) {
   if (title==undefined) title = '';
   $('<div class="dialog" title="' + title + '"><p>' + msg + '</p></div>').dialog({
      modal: true,
      show: 'fade',
      hide: 'fade',
      dialogClass: 'alert',
      buttons: {
        'OK': function() {
           $(this).dialog('close');
        }
      }
   });
}

// show a text message
function iam_showTheNotice(msg) {
  iam_showTheMessage('<span style="font-size: larger" tabindex="0">' + msg + '</span>');
}

// xmlify a string
function iam_makeOkXml(str) {
   return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/'/g,'&apos;').replace(/"/g,'&quot;');
}

/*
 * read/write functions
 */

// GET a resource
// dataType = 'xml', 'html', 'script', 'json', 'jsonp', 'text'

function iam_getRequest(url, headers, type, handler) {
   console.log('get request');
   $.ajax(url, {
     headers: headers,
     dataType: type,
     failOk: true,
     success: handler,
     error: function(data, args) {
        console.log('xhr error status: ' + args.xhr.status);
        console.log(data);
        console.log(args.xhr.responseText);
        // _showAlertFromXmlData(args.xhr.responseText);
      }
   });
}


// PUT a resource

function iam_putRequest(url, headers, putdata, type, handler) {
   document.body.style.cursor = 'wait';
   $.ajax(url, {
     headers: headers,
     dataType: type,
     data: putdata,
     failOk: true,
     success: function(data, status) {
        document.body.style.cursor = 'default';
        if (handler!=null) handler(data,status);
      },
     error: function(data, status, obj) {
        console.log('xhr error status: ' + status);
        console.log(data);
        console.log(obj.xhr.responseText);
        // _showAlertFromXmlData(args.xhr.responseText);
        document.body.style.cursor = 'default';
      }
   });
}

// DELETE a resource

function iam_deleteRequest(url, headers, type, handler) {
   document.body.style.cursor = 'wait';
   $.ajax(url, {
     type: 'DELETE',
     headers: headers,
     dataType: type,
     failOk: true,
     sucess: function(data, status) {
        document.body.style.cursor = 'default';
        if (postRequest!=null) postRequest(data, status);
      },
     error: function(data, status) {
        console.log('error' + status);
        console.log(data);
        // _showAlertFromXmlData(args.xhr.responseText);
        document.body.style.cursor = 'default';
      }
   });
}



