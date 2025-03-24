import pygame
from util.grefs import grefs

class Inventory:
    def __init__(self):
        pygame.init()
        self.window = grefs["main"].window

        self.base_image = pygame.image.load("assets\images\gui\inventory.png").convert_alpha()
        self.base_image.blit(pygame.transform.scale(pygame.image.load("assets\images\entites\player\Blue\idle.png").subsurface(0,0,16,16),(32,32)),(34,30))
        self.image = self.base_image.copy()
        self.sprite_sheet = pygame.image.load("assets/images/items_sheet.png").convert_alpha()
        self.sheet = self.load_sprites()

        self.canToggle = True

        self.positions = {
            "Helemt": (12, 27), "Chestplate": (12, 51),
            "Primary": (72, 27), "Secondary": (72, 51),
            **{i: (12 + (i % 4) * 20, 95 + (i // 4) * 20) for i in range(20)}
        }

        self.x = 320 - self.image.get_width()
        self.showing = False
        self.inv = [9,112,113,54,124,134,125,66,55,27]+[None] * 10  # Ensure inventory has fixed size
        self.equipped = {"Helemt": None, "Chestplate": None, "Primary": None, "Secondary": None}

        self.valid_items = {
            "Helemt": [1],
            "Chestplate": [122,123,124,125,126,127,128,129,130],
            "Primary": [2,3,4,5,6,7,8,9,62,63,64,65,66,67,68,69,22,23,24,25,26,27,28,29],
            "Secondary": [52,53,54,55,56,57,58,59,134]
        }

        self.dragging_item = None
        self.dragging_origin = None
        self.update_inventory()

    def load_sprites(self):
        sprites = {}
        for y in range(22):
            for x in range(22):
                sprite_id = y * x + x + 1
                sprites[sprite_id] = self.sprite_sheet.subsurface(pygame.Rect(x * 16, y * 16, 16, 16))
        return sprites

    def update_inventory(self):
        self.image = self.base_image.copy()
        for slot, item_id in self.equipped.items():
            if item_id in self.sheet and slot in self.positions:
                self.image.blit(self.sheet[item_id], self.positions[slot])
        for index, item_id in enumerate(self.inv):
            if item_id is not None and item_id in self.sheet and index in self.positions:
                self.image.blit(self.sheet[item_id], self.positions[index])

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.start_drag()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.drop_item()

    def start_drag(self):
        mouse_pos = grefs["MouseMachine"].mouse_stuff["pos"]
        print("A")
        for slot, pos in self.positions.items():
            slot_rect = pygame.Rect(pos[0] + self.x, pos[1], 16, 16)
            if slot_rect.collidepoint(mouse_pos):
                if isinstance(slot, int) and slot < len(self.inv) and self.inv[slot] is not None:
                    self.dragging_item = self.inv[slot]
                    self.dragging_origin = slot
                    self.inv[slot] = None
                elif slot in self.equipped and self.equipped[slot] is not None:
                    self.dragging_item = self.equipped[slot]
                    self.dragging_origin = slot
                    self.equipped[slot] = None
                break


    def drop_item(self):
        mouse_pos = grefs["MouseMachine"].mouse_stuff["pos"]
        if self.dragging_item is None:
            return  # If no item is being dragged, do nothing

        original_slot = self.dragging_origin  # Remember the original slot of the dragged item
        item_returned = False  # Flag to check if the item was successfully placed

        # Loop through all the available slots (inventory and equipment)
        for slot, pos in self.positions.items():
            slot_rect = pygame.Rect(pos[0] + self.x, pos[1], 16, 16)

            if slot_rect.collidepoint(mouse_pos):  # Check if the mouse is over this slot

                # If the dragged item is dropped back into the same slot, return it
                if slot == original_slot:
                    if isinstance(slot, int):  # Inventory slot
                        self.inv[slot] = self.dragging_item
                    else:  # Equipment slot
                        self.equipped[slot] = self.dragging_item
                    item_returned = True
                    break  # Stop further checks, since item is back in the original place

                # Handling dropping into an inventory slot
                if isinstance(slot, int):  # Inventory slot
                    if self.inv[slot] is None:  # Empty inventory slot
                        self.inv[slot] = self.dragging_item
                    else:  # Inventory slot is occupied, swap with existing item
                        if isinstance(original_slot, int):  # Both items are from inventory
                            self.inv[slot], self.inv[original_slot] = self.dragging_item, self.inv[slot]
                        else:  # Swapping equipped item with an inventory item
                            equipped_item = self.inv[slot]  # The item currently in the inventory slot
                            if equipped_item in self.valid_items.get(original_slot, []):  # Is the inventory item valid for the original equipment slot?
                                self.inv[slot], self.equipped[original_slot] = self.dragging_item, equipped_item
                            else:
                                self.equipped[original_slot] = self.dragging_item
                                item_returned = True
                                break
                    item_returned = True

                # Handling dropping into an equipment slot
                elif isinstance(slot, str):  # Equipment slot
                    current_item = self.equipped[slot]  # The item currently equipped in the slot
                    valid_for_slot = self.dragging_item in self.valid_items.get(slot, [])  # Is the dragged item valid for this equipment slot?
                    valid_for_original = current_item is None or self.dragging_item in self.valid_items.get(slot, [])  # Is the dragged item valid for the equipment slot?

                    # Proceed with swap if both items are valid for the slots they are moving to
                    if valid_for_slot and valid_for_original:
                        self.equipped[slot] = self.dragging_item  # Place the dragged item into the equipment slot

                        # If there was an item in the equipment slot before, move it back to inventory
                        if current_item is not None:
                            if isinstance(original_slot, int):  # If the dragged item came from the inventory
                                self.inv[original_slot] = current_item  # Put the replaced item back into inventory
                            else:  # If the dragged item came from another equipment slot
                                self.equipped[original_slot] = current_item  # Swap the two equipment items
                        item_returned = True
                    break  # Stop checking further slots after a valid swap is found

        # If no valid placement was found, return the dragged item to its original slot
        if not item_returned:
            if isinstance(original_slot, int):  # Dragged item was in the inventory
                self.inv[original_slot] = self.dragging_item
            else:  # Dragged item was in an equipment slot
                self.equipped[original_slot] = self.dragging_item

        # Reset dragging state
        self.dragging_item = None
        self.dragging_origin = None

        # Update the inventory view to reflect the changes
        self.update_inventory()

   
    def draw(self):
        self.window.blit(self.image, (self.x, 0))
        if self.dragging_item and self.dragging_item in self.sheet:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.window.blit(self.sheet[self.dragging_item], (mouse_x - 8, mouse_y - 8))

    def toggle(self):
        self.showing = not self.showing

    def add_item(self, item_id):
        #Adds an item to the first available inventory slot, if space is available.
        for i in range(len(self.inv)):
            if self.inv[i] is None:
                self.inv[i] = item_id
                self.update_inventory()
                return True  # Successfully added item
        return False  # Inventory full
    
    def update(self):
        if grefs["EventMachine"].key_states.get("keyTabDown",False) and self.canToggle == True:
            self.toggle()
            self.canToggle = False
        elif not grefs["EventMachine"].key_states.get("keyTabDown",False):
            self.canToggle = True

        if self.showing:
            self.handle_event()
            self.draw()

