from components.create_pin.pin_create import pin_create

def pin_create_controller(type_of_execution, thinking_model, browser_tab, title=None):
        """Create pin from ai prompt gen to image create in ideogram"""
        type_of_execution = "api service|web service"
        thinking_model = "thinking model|normal model"
        browser_tab = "season|red"
        title = ""
        
        # Execute the task
        # play_audio('audio/create_image_start_en.wav')
        pin_create(
            type_of_execution=type_of_execution,
            thinking_model=thinking_model,
            browser_tab=browser_tab,
            title=title
        )