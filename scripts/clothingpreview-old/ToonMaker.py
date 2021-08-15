from direct.actor.Actor import Actor

class ToonMaker:

	def ToonMaker(self, legs, torso, head, shirtText, sleeveText, pantsText, number, gender):
		if gender == 'm':
			gender = 'shorts'
		elif gender == 'f':
			gender = 'skirt'
		self.Toon = Actor(
		{'legs': 'phase_3/models/char/tt_a_chr_dg%s_shorts_legs_1000.bam' % (legs),
		'torso': 'phase_3/models/char/tt_a_chr_dg%s_%s_torso_1000.bam' % (torso, gender),
		'head': 'phase_3/models/char/tt_a_chr_dg%s_shorts_head_1000.bam' % (head)},
		{'legs': {'neutral': 'phase_3/models/char/tt_a_chr_dg%s_shorts_legs_neutral.bam' % (legs)},
		'torso': {'neutral': 'phase_3/models/char/tt_a_chr_dg%s_%s_torso_neutral.bam' % (torso, gender)},
		'head': {'neutral': 'phase_3/models/char/tt_a_chr_dg%s_shorts_head_neutral.bam' % (head)}})
		self.Toon.reparentTo(render)
		self.Toon.attach("head", "torso", "def_head")
		self.Toon.attach("torso", "legs", "joint_hips")
		self.Toon.loop('neutral')
		self.Toon.setBlend(frameBlend = True)
		self.Toon.find('**/hands').setColor(1,1,1,1)
		self.Toon.find('**/shoes').removeNode()
		self.Toon.find('**/boots_short').removeNode()
		self.Toon.find('**/boots_long').removeNode()

		shirt = loader.loadTexture(shirtText)
		sleeve = loader.loadTexture(sleeveText)
		pants = loader.loadTexture(pantsText)
		self.Toon.find('**/torso-top').setTexture(shirt, 1)
		self.Toon.find('**/sleeves').setTexture(sleeve, 1)
		self.Toon.find('**/torso-bot').setTexture(pants, 1)

		fur = (.75, .25, .25, 1)
		self.Toon.find('**/feet').setColor(fur)
		self.Toon.find('**/legs').setColor(fur)
		self.Toon.find('**/arms').setColor(fur)
		self.Toon.find('**/neck').setColor(fur)
		self.Toon.find('**/head').setColor(fur)
		self.Toon.find('**/head-front').setColor(fur)
		self.Toon.setPos(number, 0, 0)
		self.Toon.setH(180)

		Hat = loader.loadModel('phase_4/models/accessories/tt_m_chr_avt_acc_hat_bowler.bam')
		Hat.setColor(1)
		Hat.reparentTo(self.Toon.find('**/head'))
		Hat.setZ(0.30)
		Hat.setHpr(180.00, 330.00, 0.00)
		Hat.setScale(0.35)
		self.Toon.find('**/head').removeNode()
		self.Toon.find('**/head-front').removeNode()
		self.Toon.find('**/muzzle').removeNode()
		self.Toon.find('**/nose').removeNode()
		self.Toon.find('**/eyes').removeNode()
		self.Toon.find('**/ears').removeNode()

