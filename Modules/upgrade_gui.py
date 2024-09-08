import pygame
import pygame_gui

pygame.init()

class Upgrade():
    def __init__(self, categories : dict, items : dict = {}):
        self.categories = categories
        self.items = items
    
    def target(self, category : str, target : str, index : int = None):
        result = []
        for c in self.categories[category]:
            if c == target:
                result.append(c)
            else:
                pass
        try:
            result.append(str(self.items[target]["Cost"]))
            result.append(self.items[target]["Description"])
            result.append(str(self.items[target]["DMG"]))
        except KeyError:
            print("Key Error")
        
        if index == None:
            return result
        else:
            return result[index]
    
    def change_value(self, category : str, target : str, index : int, newval):
        result = self.target(category, target)
        result[index] = newval

        return result

    def return_items(self):
        keys = []
        for key in self.items.keys():
            keys.append(key)
        return keys

    def return_categories(self):
        keys = []
        for key in self.categories.keys():
            keys.append(key)
        return keys

        
class UpgradeGUI():
    def __init__(self,screen, dropdown_list : list, x : int, y : int, width : int, height : int,):
        self.screen = screen
        self.gui_manager = pygame_gui.UIManager(pygame.display.get_window_size())

        self.dropdown_menu = pygame_gui.elements.UIDropDownMenu(
            options_list=dropdown_list,
            starting_option=dropdown_list[0],
            relative_rect=pygame.Rect((x, y), (width, height)),
            manager=self.gui_manager,
            )
        self.dropdown_menu.border_width = 5
        self.dropdown_menu.expand_on_option_click = False

    def event_handling(self, event):
        self.gui_manager.process_events(event)
    
    def return_selection(self):
        return self.dropdown_menu.selected_option

    def update(self):
        self.gui_manager.update(pygame.time.get_ticks() / 1000.0)
        self.gui_manager.draw_ui(self.screen)
        
# categories = {
#   "Weapons" : ["Sword", "Gun", "Bow"],
#   "Armor" : ["WIP"]
# }
# weapons = {
#     "Cuffs" : {"Cost" : 400, "Description" : "A weapon that can be dangerous when wielded by a strong-man | +5 DMG", "DMG" : 5},
#     "Old Boxing Gloves" : {"Cost" : 250, "Description" : "From back when you were in your boxing phase | +1 DMG", "DMG" : 1},
#     "Toy Hammer" : {"Cost" : 100, "Description" : "Memories | +0.5 DMG", "DMG" : 0.5}
# }
# armor = {
#     "It's a work in progress" : {"Cost" : 999999999999, "Description" : "Wait a few years", "DMG" : 0}
# }

# categories_upg = Upgrade(categories)
# weapons_upg = Upgrade(categories, weapons)
# armor_upg = Upgrade(categories, armor)

# print(weapons_upg.target("Weapons", "Cuffs", 2))

# listting = categories_upg.return_categories()
# weapons_list = weapons_upg.return_items()
# armor_list = armor_upg.return_items()

# main_gui = UpgradeGUI(screen, listting, 0, 100, 200, 50)
# weapons_gui = UpgradeGUI(screen, weapons_list, 200, 100, 200, 50)
# armor_gui = UpgradeGUI(screen, armor_list, 200, 100, 200, 50)

# button = button.Button(screen, 0, 0, 50, 50, (100, 200, 100), None)
# var = None
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             break
#         main_gui.event_handling()
#         weapons_gui.event_handling()
#         armor_gui.event_handling()
    
    
#     screen.fill((255,255,255))
#     main_gui.update()
#     if main_gui.return_selection() == "Armor":
#         armor_gui.update()
#         armor_descr = font.render(armor_upg.target(main_gui.return_selection(), armor_gui.return_selection(), 1), True, (0,0,0), (200, 200, 200))
#         screen.blit(armor_descr, (0, 500))
#     elif main_gui.return_selection() == "Weapons":
#         weapons_gui.update()
#         weapons_descr = font.render(weapons_upg.target(main_gui.return_selection(), weapons_gui.return_selection(), 1), True, (0,0,0), (200, 200, 200))
#         screen.blit(weapons_descr, (0, 500))
    
#     button.draw()
#     if button.pressed:
#         if main_gui.return_selection() == "Armor":
#             var = armor_gui.return_selection()
#         elif main_gui.return_selection() == "Weapons":
#             var = weapons_gui.return_selection()
#         break

#     pygame.display.flip()
#     clock.tick(60)

# print(var)