# ----------------------------------------------------------------
# Oh hey there! You found the source code for the PygameGUI library!
# If you are lost and don't know how to use the library, check out the documentation at https://tbf3d.github.io/pygameui/
# Or if you know what you are doing, feel free to look around the code and see how it works! Or even contribute to the project!
# ----------------------------------------------------------------

import pygame, re
from time import time

pygame.init()

VERSION = 1.25

class Text():
    def __init__(self, position: tuple, content:str, color=(255, 255, 255), centerMode = True, fontName = "freesansbold.ttf", fontSize = 20):
        # Basic variables
        # Pos
        self.x, self.y = position
        # Show, if false the text will not be drawn
        self.hide = False
        # Font
        self.fontName = fontName
        self.fontSize = fontSize
        self.font = pygame.font.SysFont(self.fontName, self.fontSize)  # Load font
        # Text
        self.color = color
        self.content = content
        self.text = self.font.render(self.content, True, color) # Create surface object
        self.textRect = self.text.get_rect() # Get rect of text
        # centerMode
        self.centerMode = centerMode
        # Position textRect based on centerMode
        self.textRect.topleft = (self.x - (self.textRect.width // 2), self.y - (self.textRect.height // 2)) if self.centerMode else (self.x, self.y)
        
        # Other moving variables
        # Flowing
        self.flowing = False
        self.currentFlowPos = None
        self.otherFlowPos = None
        self.Xstep = 0
        self.Ystep = 0
        # Jumping
        self.jumping = False
        self.currentJumpPos = None
        self.otherJumpPos = None
        self.frames = 0
        self.frames_counter = 0
    
    def hide_toggle(self):
        self.hide = not self.hide

    def jump_toggle(self):
        self.jumping = not self.jumping
    
    def flow_toggle(self):
        self.flowing = not self.flowing

    # Makes it simple to get the position of the element (center or topleft)
    def get_pos(self):
        if self.centerMode:
            return self.rect.center
        else:
            return self.rect.topleft

    def change(self, newContent = None, newColor = None, newFontName = None, newFontSize = None):
        # If no new values are given, the old ones will be used
        if not newContent: newContent = self.content
        if not newColor: newColor = self.color
        if not newFontName: newFontName = self.fontName
        if not newFontSize: newFontSize = self.fontSize

        # Create new surface object 
        self.font = pygame.font.SysFont(newFontName, newFontSize)  # Load font
        self.text = self.font.render(newContent, True, newColor)
        self.textRect = self.text.get_rect() # Get rect
        # centerMode
        self.textRect.topleft = (self.x - (self.textRect.width // 2), self.y - (self.textRect.height // 2)) if self.centerMode else (self.x, self.y)

        # Store the new values
        self.content = newContent
        self.color = newColor
        self.fontName = newFontName
        self.fontSize = newFontSize

    # Draws text on screen if not hidden
    def draw(self, win):
        if not self.hide: win.blit(self.text, self.textRect)
    
    # Updates and moves the text if needed
    def update(self):
        if self.flowing: # If flowing
            # Check if flow has reached a flowpoint
            if self.centerMode: # If centermode is activated we will use the rects centerposition, if not the topleft
                if (self.Xstep == 0 or self.Ystep == 0):
                    if ((self.Xstep > 0) and (self.textRect.centerx > self.currentFlowPos[0])) or ((self.Xstep < 0) and (self.textRect.centerx < self.currentFlowPos[0])) or ((self.Ystep < 0) and (self.textRect.centery < self.currentFlowPos[1])) or ((self.Ystep > 0) and (self.textRect.centery > self.currentFlowPos[1])):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
                else:
                    if (((self.Xstep > 0) and (self.textRect.centerx > self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.textRect.centery > self.currentFlowPos[1]))) or (((self.Xstep > 0) and (self.textRect.centerx > self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.textRect.centery < self.currentFlowPos[1]))) or (((self.Xstep < 0) and (self.textRect.centerx < self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.textRect.centery > self.currentFlowPos[1])))or (((self.Xstep < 0) and (self.textRect.centerx < self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.textRect.centery < self.currentFlowPos[1]))):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
            else:
                if (self.Xstep == 0 or self.Ystep == 0):
                    if ((self.Xstep > 0) and (self.textRect.x > self.currentFlowPos[0])) or ((self.Xstep < 0) and (self.textRect.x < self.currentFlowPos[0])) or ((self.Ystep < 0) and (self.textRect.y < self.currentFlowPos[1])) or ((self.Ystep > 0) and (self.textRect.y > self.currentFlowPos[1])):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
                else:
                    if (((self.Xstep > 0) and (self.textRect.x > self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.textRect.y > self.currentFlowPos[1]))) or (((self.Xstep > 0) and (self.textRect.x > self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.textRect.y < self.currentFlowPos[1]))) or (((self.Xstep < 0) and (self.textRect.x < self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.textRect.y > self.currentFlowPos[1])))or (((self.Xstep < 0) and (self.textRect.x < self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.textRect.y < self.currentFlowPos[1]))):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos

            self.move(self.Xstep, self.Ystep) # Apply movement
        
        elif self.jumping: # If jumping
            self.frames_counter += 1 # Increase frame counter
            if self.frames_counter >= self.frames: # If it has gone enough time to switch position
                self.move_to(self.otherJumpPos[0], self.otherJumpPos[1]) # Apply movement
                self.currentJumpPos, self.otherJumpPos = self.otherJumpPos, self.currentJumpPos
                self.frames_counter = 0 # Reset counter

    # Moves to specific cordinates
    def move_to(self, x: int, y: int):
        if self.centerMode:
            self.x = x - (self.textRect.width // 2)
            self.y = y - (self.textRect.height // 2)
            self.textRect.topleft = (self.x, self.y)
        else:
            self.x, self.y = x, y
            self.textRect.topleft = (self.x, self.y)
    
    # Moves in x and y direction
    def move(self, xMovement: float, yMovement: float):
        # Used to make small movements posible (self.x is a float, self.textRect.x is an int)
        self.x += xMovement
        self.y += yMovement
        self.textRect.x = self.x
        self.textRect.y = self.y

    # Returns if the text is hovered
    def is_hovered(self):
        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.textRect.collidepoint(mouse_pos):
            return True 

    # Flow lets the text flow between two points
    def flow(self, position1: tuple, position2: tuple, iterations: int):
        # Move to flowpoint
        self.move_to(position1[0], position1[1])
        # Set flowpostions
        self.otherFlowPos, self.currentFlowPos = position1, position2 
        # Get amount to move per iteration
        Xdistance, Ydistance = (position2[0] - position1[0]), (position2[1] - position1[1])
        self.Xstep = Xdistance / iterations
        self.Ystep = Ydistance / iterations
        # Activate flowing
        self.flowing = True
    
    # Jump lets the user toggle the text between two points on a userSpecified timer
    def jump(self, position1: tuple, position2: tuple, frames: int):
        # Move to jumppoint
        self.move_to(position1[0], position1[1])
        # Set jumpPostions
        self.otherJumpPos, self.currentJumpPos = position2, position1
        # Frames
        self.frames = frames
        # Activate jumping
        self.jumping = True

class Element():     
    def __init__(self, position: tuple, content=None, textColor=(231, 111, 81), centerText=True, centerMode=True, fontName="freesansbold.ttf", fontSize=20, rectWidth=200, rectHeight=75, rectColor=(233, 196, 106), rectBorderRadius=10):
        # Common variables
        self.centerMode = centerMode
        self.content = content
        # Rect
        self.rectWidth = rectWidth
        self.rectHeight = rectHeight
        # Show
        self.hide = False
        self.sizeMultiplier= 1
        # Flowing
        self.flowing = False
        self.currentFlowPos = None
        self.otherFlowPos = None
        self.Xstep = 0
        self.Ystep = 0
        # Jumping
        self.jumping = False
        self.currentJumpPos = None
        self.otherJumpPos = None
        self.frames = 0
        self.frames_counter = 0
        # Clicking
        self.clicked = True

        if isinstance(self.content, str):
            self.type = "text"
            # Pos
            self.x, self.y = (position[0] - (rectWidth // 2), position[1] - (rectHeight // 2)) if self.centerMode else (position[0], position[1])
            # Rect
            self.rect = pygame.rect.Rect(self.x, self.y, rectWidth, rectHeight)
            self.rectColor = rectColor
            self.borderRadius = rectBorderRadius
            # Load font
            self.fontName = fontName
            self.fontSize = fontSize
            self.font = pygame.font.SysFont(self.fontName, self.fontSize)  # Load font
            # Text
            self.centerText = centerText
            self.textColor = textColor
            self.text = self.font.render(content, True, textColor) # Create surface object
            self.textRect = self.text.get_rect() # Get rect
            # centering the text
            if centerText: self.textRect.center = self.rect.center
            else: self.textRect.topleft = self.rect.topleft
        # If there is an image
        elif self.content:
            self.type = "image"
            try:
                self.content = pygame.transform.scale(self.content, (self.rectWidth, self.rectHeight))
                self.rect = self.content.get_rect()
            except:
                raise Exception(f"{self.content} is not a pygame image")
            
            if self.centerMode:
                # Pos
                self.rect.center = (position[0], position[1])
                # Pos
                self.x, self.y = self.rect.center
            else:
                self.rect.topleft = (position[0], position[1])
                self.x, self.y = self.rect.topleft
        # If there is no content (only a rectangle)
        else:
            self.type = "rectangle"
            # Pos
            self.x, self.y = (position[0] - (self.rectWidth // 2), position[1] - (self.rectHeight // 2)) if self.centerMode else (position[0], position[1])
            # Rect
            self.rect = pygame.rect.Rect(self.x, self.y, self.rectWidth, self.rectHeight)
            self.borderRadius = rectBorderRadius
            self.rectColor = rectColor

    # Makes it simple to get the position of the element (center or topleft)
    def get_pos(self):
        if self.centerMode:
            return self.rect.center
        else:
            return self.rect.topleft

    # Not done pos wrong
    def change(self, newContent = None, newTextColor = None, newFontName = None, newFontSize = None, newRectColor = None, newRectWidth = None, newRectHeight = None, newRectBorderRadius = None):
        if self.type == "text":
            # If no new values are given, the old ones will be used
            if not newContent: newContent = self.content
            if not newTextColor: newTextColor = self.textColor
            if not newFontName: newFontName = self.fontName
            if not newFontSize: newFontSize = self.fontSize
            if not newRectColor: newRectColor = self.rectColor
            if not newRectWidth: newRectWidth = self.rectWidth
            if not newRectHeight: newRectHeight = self.rectHeight
            if not newRectBorderRadius: newRectBorderRadius = self.borderRadius

            # Rect
            self.rect = pygame.rect.Rect(self.x, self.y, newRectWidth, newRectHeight)

            self.rectColor = newRectColor
            self.borderRadius = newRectBorderRadius

            # Create new surface object 
            self.font = pygame.font.SysFont(newFontName, newFontSize)  # Load font
            self.text = self.font.render(newContent, True, newTextColor)
            self.textRect = self.text.get_rect() # Get rect
            if self.centerText: self.textRect.center = self.rect.center
            else: self.textRect.topleft = self.rect.topleft


            # Store the new values
            self.content = newContent
            self.textColor = newTextColor
            self.fontName = newFontName
            self.fontSize = newFontSize
            self.rectWidth = newRectWidth
            self.rectHeight = newRectHeight
            self.rectBorderRadius = newRectBorderRadius
        elif self.type == "image":
            if not newContent: newContent = self.content
            if not newRectWidth: newRectWidth = self.rectWidth
            if not newRectHeight: newRectHeight = self.rectHeight

            try:
                self.content = pygame.transform.scale(newContent, (newRectWidth, newRectHeight))
                lastRect = self.rect
                self.rect = self.content.get_rect()
                self.rect.topleft = lastRect.topleft
            except:
                raise Exception(f"{self.content} is not a pygame image")

            # Store the new values
            self.content = newContent
            self.rectWidth = newRectWidth
            self.rectHeight = newRectHeight
        elif self.type == "rectangle":
            if not newRectColor: newRectColor = self.rectColor
            if not newRectWidth: newRectWidth = self.rectWidth
            if not newRectHeight: newRectHeight = self.rectHeight
            if not newRectBorderRadius: newRectBorderRadius = self.borderRadius

            self.rect = pygame.rect.Rect(self.rect.x, self.rect.y, newRectWidth, newRectHeight)
            self.rectColor = newRectColor
            self.borderRadius = newRectBorderRadius

            # Store the new values
            self.rectWidth = newRectWidth
            self.rectHeight = newRectHeight
            self.rectBorderRadius = newRectBorderRadius

    def hide_toggle(self):
        self.hide = not self.hide

    def jump_toggle(self):
        self.jumping = not self.jumping
    
    def flow_toggle(self):
        self.flowing = not self.flowing

    def draw(self, win):
        if not self.hide:
            # If the element has text
            if self.type == "text":
                # Draw text
                pygame.draw.rect(win, self.rectColor, self.rect, border_radius = self.borderRadius)
                win.blit(self.text, self.textRect)
            # If the element has an image
            elif self.type == "image":
                # Draw img
                win.blit(self.content, self.rect)
            # If the element is a just rectangle
            elif self.type == "rectangle":
                pygame.draw.rect(win, self.rectColor, self.rect, border_radius = self.borderRadius)

    def is_hovered(self):
        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            return True 

    def is_clicked(self, clickable_elements: list):
        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0] == 1: # == 1 is left click
                return True
        else:
            for element in clickable_elements: # Checks if user is howering any other buttons
                if element.rect.collidepoint(mouse_pos):
                    break
            else: # If not howering any other buttons: set cursor to arrow
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def was_clicked(self, clickable_elements: list):
        action = False

        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # == 1 is left click
                self.clicked = True
                action = True
        else:
            for element in clickable_elements:
                if element.rect.collidepoint(mouse_pos):
                    break
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        if pygame.mouse.get_pressed()[0] == 0: #  No mousebuttons down
            self.clicked = False

        return action

    # Updates and moves the text if needed
    def update(self):
        if self.flowing: # If flowing
            # Check if flow has reached a flowpoint
            if self.centerMode: # If centermode is activated we will use the rects centerposition, if not the topleft
                if (self.Xstep == 0 or self.Ystep == 0):
                    if ((self.Xstep > 0) and (self.rect.centerx > self.currentFlowPos[0])) or ((self.Xstep < 0) and (self.rect.centerx < self.currentFlowPos[0])) or ((self.Ystep < 0) and (self.rect.centery < self.currentFlowPos[1])) or ((self.Ystep > 0) and (self.rect.centery > self.currentFlowPos[1])):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
                else:
                    if (((self.Xstep > 0) and (self.rect.centerx > self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.centery > self.currentFlowPos[1]))) or (((self.Xstep > 0) and (self.rect.centerx > self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.centery < self.currentFlowPos[1]))) or (((self.Xstep < 0) and (self.rect.centerx < self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.centery > self.currentFlowPos[1])))or (((self.Xstep < 0) and (self.rect.centerx < self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.centery < self.currentFlowPos[1]))):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
            else:
                if (self.Xstep == 0 or self.Ystep == 0):
                    if ((self.Xstep > 0) and (self.rect.x > self.currentFlowPos[0])) or ((self.Xstep < 0) and (self.rect.x < self.currentFlowPos[0])) or ((self.Ystep < 0) and (self.rect.y < self.currentFlowPos[1])) or ((self.Ystep > 0) and (self.rect.y > self.currentFlowPos[1])):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
                else:
                    if (((self.Xstep > 0) and (self.rect.x > self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.y > self.currentFlowPos[1]))) or (((self.Xstep > 0) and (self.rect.x > self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.y < self.currentFlowPos[1]))) or (((self.Xstep < 0) and (self.rect.x < self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.y > self.currentFlowPos[1])))or (((self.Xstep < 0) and (self.rect.x < self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.y < self.currentFlowPos[1]))):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos

            self.move(self.Xstep, self.Ystep) # Apply movement
        
        elif self.jumping: # If jumping
            self.frames_counter += 1 # Increase frame counter
            if self.frames_counter >= self.frames: # If it has gone enough time to switch position
                self.move_to(self.otherJumpPos[0], self.otherJumpPos[1]) # Apply movement
                self.currentJumpPos, self.otherJumpPos = self.otherJumpPos, self.currentJumpPos
                self.frames_counter = 0 # Reset counter

    # Moves to specific cordinates
    def move_to(self, x: int, y:  int):
        if self.centerMode:
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
            if self.type == "text": # Only affect the textRect if there is text
                if self.centerText:
                    self.textRect.center = self.rect.center
                else:
                    self.textRect.topleft = self.rect.topleft
        else:
            self.rect.topleft = (x, y)
            self.x, self.y = self.rect.topleft
            if self.type == "text": # Only affect the textRect if there is text
                if self.centerText:
                    self.textRect.center = self.rect.center
                else:
                    self.textRect.topleft = self.rect.topleft
    
    # Moves in x and y direction
    def move(self, xMovement: float, yMovement: float):
        # Used to make small movements posible (self.x is a float, self.textRect.x is an int)
        self.x += xMovement
        self.y += yMovement
        if self.centerMode:
            self.rect.center = (self.x, self.y)
            if self.type == "text": # Only affect the textRect if there is text
                if self.centerText:
                    self.textRect.center = self.rect.center
                else:
                    self.textRect.topleft = self.rect.topleft
        else:
            self.rect.topleft = (self.x, self.y)
            if self.type == "text": # Only affect the textRect if there is text
                if self.centerText:
                    self.textRect.center = self.rect.center
                else:
                    self.textRect.topleft = self.rect.topleft

    # Flow lets the text flow between two points
    def flow(self, position1: tuple, position2: tuple, iterations: int):
        # Move to flowpoint
        self.move_to(position1[0], position1[1])
        # Set flowpostions
        self.otherFlowPos, self.currentFlowPos = position1, position2 
        # Get amount to move per iteration
        Xdistance, Ydistance = (position2[0] - position1[0]), (position2[1] - position1[1])
        self.Xstep = Xdistance / iterations
        self.Ystep = Ydistance / iterations
        # Activate flowing
        self.flowing = True
    
    # Jump lets the user toggle the text between two points on a userSpecified timer
    def jump(self, position1: tuple, position2: tuple, iterations: int):
        # Move to jumppoint
        self.move_to(position1[0], position1[1])
        # Set jumpPostions
        self.otherJumpPos, self.currentJumpPos = position2, position1
        # Frames
        self.frames = iterations
        # Activate jumping
        self.jumping = True

class Input():
    def __init__(self, position: tuple, fontName = "freesansbold.ttf", fontSize = 30, exampleContent = "Click me to input!", prefilledContent = "", characterLimit = 100, normalTextColor = (231, 111, 81), exampleTextColor = (100, 100, 100), rectWidth = 200, rectHeight = 50, rectColorActive = (233, 196, 106), rectColorPassive = (200, 200, 200), rectBorderRadius = 1, rectBorderWidth = 5, centerMode = True):
        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
        
        # Create position variables and font
        self.centerMode = centerMode
        # Pos
        self.x, self.y = (position[0] - (rectWidth // 2), position[1] - (rectHeight // 2)) if centerMode else (position[0], position[1])
        # Rect
        self.rect = pygame.rect.Rect(self.x, self.y, rectWidth, rectHeight)
        self.borderRadius = rectBorderRadius
        self.rectBorderWidth = rectBorderWidth
        self.rectColorPassive = rectColorPassive
        self.rectColorActive = rectColorActive
        # Text
        self.normalTextColor = normalTextColor
        self.exampleTextColor = exampleTextColor
        self.characterLimit = characterLimit
        self.fontName = fontName
        self.fontSize = fontSize
        self.font = pygame.font.SysFont(self.fontName, self.fontSize)  # Load font
        self.prefilledContent = prefilledContent
        self.userText = self.prefilledContent
        self.exampleContent = exampleContent
        self.userTextSurface = self.font.render(self.userText, True, self.normalTextColor) # Create surface object for the userText
        self.exampleTextSurface = self.font.render(self.exampleContent, True, self.exampleTextColor) # Create surface object the exampleText

        self.userTextRect = self.userTextSurface.get_rect() # Get rect
        self.exampleTextRect = self.exampleTextSurface.get_rect() # Get rect

        # Filter
        self.filter_mode = "isAllowed" # isAllowed or isDisallowed, if isAllowed the filter will only allow the characters in the filter, if isDisallowed the filter will disallow the characters in the filter
        self.filter = None

        # Cursor
        self.cursor_visible_timer = 60
        self.cursor_index = len(self.userText)

        # centering the text
        self.userTextRect.center = self.rect.center
        self.exampleTextRect.center = self.rect.center
        # Show
        self.hide = False
        # Flowing
        self.flowing = False
        self.currentFlowPos = None
        self.otherFlowPos = None
        self.Xstep = 0
        self.Ystep = 0
        # Jumping
        self.jumping = False
        self.currentJumpPos = None
        self.otherJumpPos = None
        self.frames = 0
        self.frames_counter = 0
        # Clicking
        self.clicked = False
        self.active = False

        # Key down
        self.key_down_dict = {} # 
        self.key_down_time = 0
        self.long_press_active = False
        self.key_down_last_frame = False
        self.min_hold_time = .5 # The minimun time between key reaction

    def hide_toggle(self):
        self.hide = not self.hide

    # Makes it simple to get the position of the element (center or topleft)
    def get_pos(self):
        if self.centerMode:
            return self.rect.center
        else:
            return self.rect.topleft

    def jump_toggle(self):
        self.jumping = not self.jumping
    
    def flow_toggle(self):
        self.flowing = not self.flowing

    def set_filter(self, filter: list, isAllowed: bool = True):
        self.filter = filter
        self.filter_mode = "isAllowed" if isAllowed else "isDisallowed"

    def get_relative_cursor_position(self) -> int:
        substring = self.userText[:self.cursor_index]
        return self.font.size(substring)[0]
    
    def get_letter_position(self, letterIndex: str) -> int:
        substring = self.userText[:letterIndex]
        return self.font.size(substring)[0] + self.userTextRect.left

    def draw(self, win):
        if not self.hide:
            if self.userText != "":
                win.blit(self.userTextSurface, self.userTextRect)
            else:
                if not self.active:
                    win.blit(self.exampleTextSurface, self.exampleTextRect)
                    
            if self.active:
                # Draw rect
                pygame.draw.rect(win, self.rectColorActive, self.rect, self.rectBorderWidth, border_radius = self.borderRadius)

                # Draw cursor and make it blink
                self.cursor_visible_timer -= 1
                if self.cursor_visible_timer > 30:
                    cursor_pos = self.get_relative_cursor_position() + self.userTextRect.left
                    pygame.draw.line(win, self.normalTextColor, (cursor_pos, self.userTextRect.top), (cursor_pos, self.userTextRect.bottom), self.fontSize // 15)
                elif self.cursor_visible_timer == 0:
                    self.cursor_visible_timer = 60

            else:
                pygame.draw.rect(win, self.rectColorPassive, self.rect, self.rectBorderWidth, border_radius = self.borderRadius)

    def get_value(self):
        return self.userText

    def backspace(self):
        if self.cursor_index == len(self.userText):
            self.userText = self.userText[0: -1]
            if self.cursor_index > 0:
                self.cursor_index -= 1
        elif self.cursor_index != 0:
            self.userText = self.userText[0: self.cursor_index - 1] + self.userText[self.cursor_index:]
            if self.cursor_index > 0:
                self.cursor_index -= 1

    def update_text(self):
        # Update the text
        self.userTextSurface = self.font.render(self.userText, True, self.normalTextColor) # Create surface object for the userText
        self.userTextRect = self.userTextSurface.get_rect() # Get rect
        self.userTextRect.center = self.rect.center

    def work(self, events: list, clickable_elements: list):
        # Make activating work
        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # == 1 is left click
                if self.active:
                    # Move cursor to the position of the mouse
                    new_cursor_index = 0
                    for letterIndex in range(len(self.userText)):
                        letterPos = self.get_letter_position(letterIndex)
                        if letterPos - (self.font.size((self.userText[letterIndex]))[0] // 2) < mouse_pos[0]:
                            new_cursor_index = letterIndex
                        
                    # If the mouse is to the right of the text
                    if (self.font.size(self.userText)[0] + self.userTextRect.left) < mouse_pos[0]:
                        new_cursor_index = len(self.userText)
                    
                    self.cursor_index = new_cursor_index
                else:
                    self.active = True
                    # Move cursor to the end of the text
                    self.cursor_index = len(self.userText)
                
                self.cursor_visible_timer = 60
                self.clicked = True
        else:
            if pygame.mouse.get_pressed()[0]: # == 1 is left click
                self.active = False
            for element in clickable_elements:
                if element.rect.collidepoint(mouse_pos):
                    break
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        if pygame.mouse.get_pressed()[0] == 0: #  No mousebuttons down
            self.clicked = False

        # Make backspace work
        inputs  = pygame.key.get_pressed()

        if self.active:
            if inputs[pygame.K_BACKSPACE]:
                if (not self.long_press_active) and (self.key_down_last_frame) and (time() - self.key_down_time > .4):
                    self.long_press_active = True
                    self.min_hold_time = .07

                if (time() - self.key_down_time > self.min_hold_time) or not self.key_down_last_frame:
                    self.backspace()
                    self.update_text()
                    self.key_down_time = time()
                    self.key_down_last_frame = True
            
            else:
                self.key_down_last_frame = False
                self.long_press_active = False
                self.min_hold_time = .5

        # Make writing work
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.active:
                    # Allow the user to paste text from clipboard
                    if event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                        pasted_text = pygame.scrap.get("text/plain;charset=utf-8").decode()
                        # Remove all non-printable characters
                        pasted_text = re.sub(r'[^\x20-\x7E]+', '', pasted_text)

                        # Filter the pasted text
                        for letter in pasted_text:
                            if self.filter_mode == "isAllowed" and letter not in self.filter:
                                pasted_text = pasted_text.replace(letter, "")
                            elif self.filter_mode == "isDisallowed" and letter in self.filter:
                                pasted_text = pasted_text.replace(letter, "")
                        # Check that the pasted text is not exceeding the character limit
                        if len(self.userText) + len(pasted_text) > self.characterLimit:
                            continue

                        self.userText = self.userText[0: self.cursor_index] + pasted_text + self.userText[self.cursor_index:]
                        # Move cursor to the end of the pasted text
                        self.cursor_index += len(pasted_text)
                    elif event.key == pygame.K_BACKSPACE:
                        pass
                    elif event.key == pygame.K_DELETE:
                        if self.cursor_index != len(self.userText):
                            self.userText = self.userText[0: self.cursor_index] + self.userText[self.cursor_index + 1:]
                    elif event.key == pygame.K_HOME:
                        self.cursor_index = 0
                    elif event.key == pygame.K_END:
                        self.cursor_index = len(self.userText)
                    elif event.key == pygame.K_TAB:
                        self.userText = self.userText[0: self.cursor_index] + "    " + self.userText[self.cursor_index:]
                        self.cursor_index += 4
                    # Allow the user to move the cursor
                    elif event.key == pygame.K_LEFT:
                        if self.cursor_index > 0:
                            self.cursor_index -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.cursor_index < len(self.userText):
                            self.cursor_index += 1
                    # Filter
                    elif self.filter and ((self.filter_mode == "isAllowed" and (event.unicode not in self.filter)) or (self.filter_mode == "isDisallowed" and (event.unicode in self.filter))): 
                        continue
                    # Allow the user to write text
                    elif (len(self.userText) <= self.characterLimit): # Keep text under character limit and don't enterperate enter as a key
                        if event.unicode and event.key != pygame.K_RETURN:
                            self.userText = self.userText[0: self.cursor_index] + event.unicode + self.userText[self.cursor_index:] # Adds the userinput to the text
                            self.cursor_index += 1

                    # Update the text
                    self.userTextSurface = self.font.render(self.userText, True, self.normalTextColor) # Create surface object for the userText
                    self.userTextRect = self.userTextSurface.get_rect() # Get rect
                    self.userTextRect.center = self.rect.center

    # Updates and moves the text if needed
    def update(self):
        if self.flowing: # If flowing
            # Check if flow has reached a flowpoint
            if self.centerMode: # If centermode is activated we will use the rects centerposition, if not the topleft
                if (self.Xstep == 0 or self.Ystep == 0):
                    if ((self.Xstep > 0) and (self.rect.centerx > self.currentFlowPos[0])) or ((self.Xstep < 0) and (self.rect.centerx < self.currentFlowPos[0])) or ((self.Ystep < 0) and (self.rect.centery < self.currentFlowPos[1])) or ((self.Ystep > 0) and (self.rect.centery > self.currentFlowPos[1])):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
                else:
                    if (((self.Xstep > 0) and (self.rect.centerx > self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.centery > self.currentFlowPos[1]))) or (((self.Xstep > 0) and (self.rect.centerx > self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.centery < self.currentFlowPos[1]))) or (((self.Xstep < 0) and (self.rect.centerx < self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.centery > self.currentFlowPos[1])))or (((self.Xstep < 0) and (self.rect.centerx < self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.centery < self.currentFlowPos[1]))):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
            else:
                if (self.Xstep == 0 or self.Ystep == 0):
                    if ((self.Xstep > 0) and (self.rect.x > self.currentFlowPos[0])) or ((self.Xstep < 0) and (self.rect.x < self.currentFlowPos[0])) or ((self.Ystep < 0) and (self.rect.y < self.currentFlowPos[1])) or ((self.Ystep > 0) and (self.rect.y > self.currentFlowPos[1])):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
                else:
                    if (((self.Xstep > 0) and (self.rect.x > self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.y > self.currentFlowPos[1]))) or (((self.Xstep > 0) and (self.rect.x > self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.y < self.currentFlowPos[1]))) or (((self.Xstep < 0) and (self.rect.x < self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.y > self.currentFlowPos[1])))or (((self.Xstep < 0) and (self.rect.x < self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.y < self.currentFlowPos[1]))):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos

            self.move(self.Xstep, self.Ystep) # Apply movement
        
        elif self.jumping: # If jumping
            self.frames_counter += 1 # Increase frame counter
            if self.frames_counter >= self.frames: # If it has gone enough time to switch position
                self.move_to(self.otherJumpPos[0], self.otherJumpPos[1]) # Apply movement
                self.currentJumpPos, self.otherJumpPos = self.otherJumpPos, self.currentJumpPos
                self.frames_counter = 0 # Reset counter

    # Moves to specific cordinates
    def move_to(self, x: int, y:  int):
        if self.centerMode:
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
            self.userTextRect.center = (x, y)
            self.exampleTextRect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
            self.x, self.y = self.rect.topleft
            self.userTextRect.topleft = (self.x, self.y)
            self.exampleTextRect.topleft = (self.x, self.y)
    
    # Moves in x and y direction
    def move(self, xMovement: float, yMovement: float):
        # Used to make small movements posible (self.x is a float, self.textRect.x is an int)
        self.x += xMovement
        self.y += yMovement
        if self.centerMode:
            self.rect.center = (self.x, self.y)
            self.userTextRect.center = (self.x, self.y)
            self.exampleTextRect.center = (self.x, self.y)
        else:
            self.rect.topleft = (self.x, self.y)
            self.userTextRect.topleft = (self.x, self.y)
            self.exampleTextRect.topleft = (self.x, self.y)
    
    def is_hovered(self):
        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            return True 

    # Flow lets the text flow between two points
    def flow(self, position1: tuple, position2: tuple, iterations: int):
        # Move to flowpoint
        self.move_to(position1[0], position1[1])
        # Set flowpostions
        self.otherFlowPos, self.currentFlowPos = position1, position2 
        # Get amount to move per iteration
        Xdistance, Ydistance = (position2[0] - position1[0]), (position2[1] - position1[1])
        self.Xstep = Xdistance / iterations
        self.Ystep = Ydistance / iterations
        # Activate flowing
        self.flowing = True
    
    # Jump lets the user toggle the text between two points on a userSpecified timer
    def jump(self, position1: tuple, position2: tuple, frames: int):
        # Move to jumppoint
        self.move_to(position1[0], position1[1])
        # Set jumpPostions
        self.otherJumpPos, self.currentJumpPos = position2, position1
        # Frames
        self.frames = frames
        # Activate jumping
        self.jumping = True
