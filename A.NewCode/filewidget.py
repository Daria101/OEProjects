class FileWidget(widgets.DOMWidget):
    _view_name = Unicode('FilePickerView', sync=True)
    value = Unicode(sync=True)
    filename = Unicode(sync=True)
    
    def __init__(self, **kwargs):
        """Constructor"""
        widgets.DOMWidget.__init__(self, **kwargs) # Call the base.
        
        # Allow the user to register error callbacks with the following signatures:
        #    callback()
        #    callback(sender)
        self.errors = widgets.CallbackDispatcher(accepted_nargs=[0, 1])
        
        # Listen for custom msgs
        self.on_msg(self._handle_custom_msg)

    def _handle_custom_msg(self, content):
        """Handle a msg from the front-end.

        Parameters
        ----------
        content: dict
            Content of the msg."""
        if 'event' in content and content['event'] == 'error':
            self.errors()
            self.errors(self)
            
%%javascript

require(["widgets/js/widget", "widgets/js/manager"], function(widget, manager){

    var FilePickerView = widget.DOMWidgetView.extend({
        render: function(){
            // Render the view.
            this.setElement($('<input />')
                .attr('type', 'file'));
        },
        
        events: {
            // List of events and their handlers.
            'change': 'handle_file_change',
        },
       
        handle_file_change: function(evt) { 
            // Handle when the user has changed the file.
            
            // Retrieve the first (and only!) File from the FileList object
            var file = evt.target.files[0];
            if (file) {

                // Read the file's textual content and set value to those contents.
                var that = this;
                var file_reader = new FileReader();
                file_reader.onload = function(e) {
                    that.model.set('value', e.target.result);
                    that.touch();
                }
                file_reader.readAsText(file);
            } else {

                // The file couldn't be opened.  Send an error msg to the
                // back-end.
                this.send({ 'event': 'error' });
            }

            // Set the filename of the file.
            this.model.set('filename', file.name);
            this.touch();
        },
    });
        
    // Register the DatePickerView with the widget manager.
    manager.WidgetManager.register_widget_view('FilePickerView', FilePickerView);
});