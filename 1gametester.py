import pygame
import pygame.mixer
pygame.mixer.init() 
pygame.init()

import serial #Import Serial Library 
ser = serial.Serial('com3',9600) #Create Serial port object called arduinoSerialData
 
def read():
    myData = ser.readline()
    myData=myData.decode()
    myData=myData[:len(myData)-2]
    print (myData)
    return(myData)
    


win = pygame.display.set_mode((500,480))
pygame.display.set_caption("My Game")

walkRight = [pygame.image.load('./images/R1.png'), pygame.image.load('./images/R2.png'), pygame.image.load('./images/R3.png'),
             pygame.image.load('./images/R4.png'), pygame.image.load('./images/R5.png'), pygame.image.load('./images/R6.png'),
             pygame.image.load('./images/R7.png'), pygame.image.load('./images/R8.png'), pygame.image.load('./images/R9.png')]

walkLeft = [pygame.image.load('./images/L1.png'), pygame.image.load('./images/L2.png'), pygame.image.load('./images/L3.png'),
            pygame.image.load('./images/L4.png'), pygame.image.load('./images/L5.png'), pygame.image.load('./images/L6.png'),
            pygame.image.load('./images/L7.png'), pygame.image.load('./images/L8.png'), pygame.image.load('./images/L9.png')]
bg = pygame.image.load('./images/bg.jpg')
char = pygame.image.load('./images/standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound("bullet.wav")
hitSound = pygame.mixer.Sound('hit.mp3')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)#repeat the song when it ends

score = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self,win):
        if self.walkCount + 1 >= 27:#9 sprites,displaying each sprite for 3 frames
            self.walkCount = 0

        if not(self.standing):
            if self.left:  
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))#indexing the correct image
                self.walkCount += 1   
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1  
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

    
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (500/2 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(2)
            i += 1  #so we can see the text on the screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
                

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x= x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('./images/R1E.png'), pygame.image.load('./images/R2E.png'), pygame.image.load('./images/R3E.png'), pygame.image.load('./images/R4E.png'), pygame.image.load('./images/R5E.png'), pygame.image.load('./images/R6E.png'), pygame.image.load('./images/R7E.png'), pygame.image.load('./images/R8E.png'), pygame.image.load('./images/R9E.png'), pygame.image.load('./images/R10E.png'), pygame.image.load('./images/R11E.png')]
    walkLeft = [pygame.image.load('./images/L1E.png'), pygame.image.load('./images/L2E.png'), pygame.image.load('./images/L3E.png'), pygame.image.load('./images/L4E.png'), pygame.image.load('./images/L5E.png'), pygame.image.load('./images/L6E.png'), pygame.image.load('./images/L7E.png'), pygame.image.load('./images/L8E.png'), pygame.image.load('./images/L9E.png'), pygame.image.load('./images/L10E.png'), pygame.image.load('./images/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
        

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1>= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))#red bar appereance
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))#50(max health) - 5*(10-(number you've been hit)
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

        

    def move(self):
        if self.vel>0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("hit")
        


def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (350, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
        
    pygame.display.update() 
    

#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 1
bullets = []
run = True

while run:
    clock.tick(27)#fps set

    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3]> goblin.hitbox[1]:#in the y coordinates
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:#in the x coordinates
                man.hit()
                score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:#in the y coordinates
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0]+goblin.hitbox[2]:#in the x coordinates
                #hitSound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))#deletes the bullet
                
        
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
        
    keys = pygame.key.get_pressed()
    '''
    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6 ,(0,0,0), facing))
    '''

    if int(read()) and shootLoop== 1:
        #bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6 ,(0,0,0), facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel: 
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.vel - man.width:  
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else: 
        man.standing = True
        man.walkCount = 0

    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.5
            man.jumpCount -= 1
        else: 
            man.jumpCount = 10
            man.isJump = False

    redrawGameWindow() 
    
    
pygame.quit()
