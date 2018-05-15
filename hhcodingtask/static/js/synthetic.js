(function($) {

    $.synthetic = function(options) {
        if (typeof(options) == "undefined" || options == null) {
            options = {};
        };

        var API = {
            options: $.extend({
                    rpc_url: "",
                    onSuccess: function(data, status) {},
                    onFailure: function(data) {},
                    onProgress: function(evt) {},
                    errorElementID: ''
                },
                options),
            get_json: function(callback, error_callback) {
                $.ajax({
                    url: API.options.rpc_url,
                    cache: false,
                    dataType: 'json',
                    beforeSend: function(xhr) {
                        // set auth token here
                    },
                    success: function(data, status) {
                        if (callback) callback(data, status);
                    }
                }).fail(function(jqxhr, textStatus, error) {
                    var err = textStatus + ', ' + error;
                    if (error != '') API.error_happened(err);
                });
            },
            post_json: function(url, form_data, headers, onSuccess, onFailure, onProgress) {
                // ``form_data`` -- instance of ``FormData``
                $.ajax({
                    url: url,
                    type: 'POST',
                    cache: false,
                    dataType: 'json',
                    data: form_data,
                    processData: false,
                    contentType: false,
                    timeout: 480000,
                    headers: headers,
                    success: function(data, status, jqXHR) {
                        if (data && data.hasOwnProperty('error')) {
                            onFailure(NaN, NaN, data);
                            return;
                        }
                        onSuccess(data, status);
                    },
                    beforeSend: function(xhr) {
                        // set auth header here
                        // xhr.setRequestHeader("authorization", "Token ...");
                    },
                    xhr: function() {
                        var req = $.ajaxSettings.xhr();
                        if (req) {
                            if (typeof req.upload == "object") {
                                req.upload.addEventListener("progress", function(evt) {
                                    onProgress(evt);
                                });
                            }
                        }
                        return req;
                    }
                }).fail(function(xhr, status, msg) {
                    var e = msg;
                    try {
                        e = $.parseJSON(xhr.responseText);
                    } catch (e) {};
                    onFailure(xhr, status, e);
                });
            },
            error_happened: function(msg) {
                var message = "Error loading content.";
                if (msg != undefined) {
                    message = msg;
                }
                $('#' + API.options.errorElementID).empty().append('<span class="err">' + message + '</span>');
            },
            get_objects_list: function() {
                API.get_json(API.options.onSuccess, API.options.onFailure);
            },
	    create_object: function(city, temperature, callback){
		var data = JSON.stringify({'city': city, 'temperature': temperature});
		API.post_json(API.options.rpc_url, data, {}, function(data, status){
		    if(callback) callback(data);
		}, function(xhr, status, msg){},  function(evt){});
	    }
        };
        return {
            list: API.get_objects_list,
	    create: API.create_object
        };
    };
})(jQuery);
