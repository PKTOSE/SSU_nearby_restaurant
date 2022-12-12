import customtkinter
import os
from PIL import Image
import getWeather, guessMenu

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("SSU Meal Proposal")
        self.geometry(f"{800}x{500}")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "cloudy.png")),
                                                 size=(26, 26))

        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "cloudy.png")),
                                                       size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))

        self.menu_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "menu.png")),
                                                 size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Weather (beta)",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.scaling_label = customtkinter.CTkLabel(self.navigation_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_label = customtkinter.CTkLabel(self.home_frame, text="날씨", font=('나눔고딕', 20), anchor="e")
        self.home_frame_label.grid(row=1, column=0, padx=50, pady=30)

        self.home_frame_weather_button = customtkinter.CTkButton(self.home_frame, text="날씨 새로고침",
                                                                 image=self.image_icon_image, compound="left",
                                                                 font=('나눔고딕', 15, "bold"), command=self.get_weather)
        self.home_frame_weather_button.grid(row=2, column=0, padx=20, pady=10)

        self.home_frame_menu_proposal = customtkinter.CTkLabel(self.home_frame, text="식당", font=('나눔고딕', 20))
        self.home_frame_menu_proposal.grid(row=3, column=0, padx=50, pady=30)

        self.home_frame_menu_button = customtkinter.CTkButton(self.home_frame, text="식당 제안 (beta)",
                                                              image=self.menu_image, compound="left",
                                                              font=('나눔고딕', 15, "bold"), command=self.get_menu)
        self.home_frame_menu_button.grid(row=4, column=0, padx=20, pady=10)

        # select default frame
        self.select_frame_by_name("home")
        self.appearance_mode_menu.set("Dark")
        self.scaling_optionemenu.set("125%")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def get_weather(self):
        celcius = getWeather.get_naver_weather()
        celcius = celcius["now_degree"]
        self.home_frame_label.configure(text=f"현재 날씨: {celcius}")


    def get_menu(self):
        proposal = guessMenu.get_rdm_from_list()
        self.home_frame_menu_proposal.configure(text=f"이곳은 어떠신가요?\n\n{proposal}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
