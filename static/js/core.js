

function loadTemplate(templateName, path, success, error) {
    var template = $('#' + templateName);
    if (template.length === 0) {
        var tmpl_string = '';

        $.ajax({
            url: path,
            method: 'GET',
            async: false, //If there is are callbacks, then make it async
            contentType: 'text',
            success: function (data) {
                tmpl_string = data;
                success && success(data);
            }, 
            error : function(data) {
            	error && error(data);
            }
        });

        $('head').append('<script id="' + 
        templateName + '" type="text/template">' + tmpl_string + '<\/script>');
    }
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/*
For serializing forms into json
*/

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

/*
    For adding the CSRF token to the backbone sync method
*/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var oldSync = Backbone.sync;
Backbone.sync = function(method, model, options){
    options.beforeSend = function(xhr){
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    };
    return oldSync(method, model, options);
};



var app = {};
app.views = {};
app.auth = {};
app.util = {};


var NiceView = Backbone.View.extend({

    evs : {
        'click .disabled' : 'nothing'
    },

    nothing : function(ev) {
        ev.stopImmediatePropagation();
    },

    pushform : function($form) {
        var $form = $form ? $form : this.$el.find('form');
        return $form.serializeObject();
    },

    popform : function(vals, $form) {
        var $form = $form? $form : this.$el.find('form');
        for(k in vals) {
            this.$el.find('[name="'+k+'"]').val(vals[k]);
        }
    },

});