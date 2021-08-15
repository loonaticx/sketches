from direct.showbase.ShowBase import ShowBase
from ToonMaker import *
from pandac.PandaModules import *

# shoutout to chris for making me this epic script like 4 years ago

Fat = ToonMaker()
Thin = ToonMaker()
Average = ToonMaker()

class Toon(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		FatToonShirt = 'shirt.png'
		FatToonSleeve = 'sleeve.png'
		FatToonPants = 'shorts.png'

		ThinToonShirt = FatToonShirt
		ThinToonSleeve = FatToonSleeve
		ThinToonPants = FatToonPants

		AverageToonShirt = FatToonShirt
		AverageToonSleeve = FatToonSleeve
		AverageToonPants = FatToonPants

		Fat.ToonMaker('s','s','s', FatToonShirt, FatToonSleeve, FatToonPants, 0, 'm')
		Thin.ToonMaker('m','m','m', ThinToonShirt, ThinToonSleeve, ThinToonPants, -3.5, 'm')
		Average.ToonMaker('l','l','l', AverageToonShirt, AverageToonSleeve, AverageToonPants, 3.5,'m')

Project = Toon()
Project.run()
