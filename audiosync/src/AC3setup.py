from Components.ActionMap import NumberActionMap
from Components.Button import Button
from Components.config import config
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.SystemInfo import SystemInfo
from Screens.Screen import Screen

from . import _
from .AC3utils import PLUGIN_BASE, PLUGIN_VERSION


class AC3LipSyncSetup(ConfigListScreen, Screen):
	skin = """
		<screen position="center,center" size="560,400" title="AC3 Lip Sync setup">
			<ePixmap pixmap="~/img/button-red.png" position="0,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />
			<ePixmap pixmap="~/img/button-green.png" position="140,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />
			<ePixmap pixmap="~/img/button-yellow.png" position="280,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />
			<ePixmap pixmap="~/img/button-blue.png" position="420,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />
			<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;20" valign="center" halign="center" backgroundColor="#9f1313" transparent="1" shadowColor="#000000" shadowOffset="-1,-1" />
			<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;20" valign="center" halign="center" backgroundColor="#1f771f" transparent="1" shadowColor="#000000" shadowOffset="-1,-1" />
			<widget name="key_yellow" position="280,0" zPosition="1" size="140,40" font="Regular;20" valign="center" halign="center" backgroundColor="#a08500" transparent="1" shadowColor="#000000" shadowOffset="-1,-1" />
			<widget name="key_blue" position="420,0" zPosition="1" size="140,40" font="Regular;20" valign="center" halign="center" backgroundColor="#18188b" transparent="1" shadowColor="#000000" shadowOffset="-1,-1" />
			<widget name="config" position="10,40" size="540,320" scrollbarMode="showOnDemand" />
			<widget name="PluginInfo" position="10,370" size="540,20" zPosition="4" font="Regular;18" foregroundColor="#cccccc" />
		</screen>"""

	def __init__(self, session, plugin_path):
		Screen.__init__(self, session)
		self.setTitle(_("AC3 Lip Sync setup"))
		self.list = [
			(_("Outer bound (+/-)"), config.plugins.AC3LipSync.outerBounds),
			(_("Step in ms for arrow keys"), config.plugins.AC3LipSync.arrowStepSize),
			(_("Wait time in ms before activation:"), config.plugins.AC3LipSync.activationDelay),
			(_("Step in ms for keys '%s'") % ("1/3"), config.plugins.AC3LipSync.stepSize13),
			(_("Step in ms for keys '%s'") % ("4/6"), config.plugins.AC3LipSync.stepSize46),
			(_("Step in ms for keys '%s'") % ("7/9"), config.plugins.AC3LipSync.stepSize79),
			(_("Step in ms for key %i") % (2), config.plugins.AC3LipSync.absoluteStep2),
			(_("Step in ms for key %i") % (5), config.plugins.AC3LipSync.absoluteStep5),
			(_("Step in ms for key %i") % (8), config.plugins.AC3LipSync.absoluteStep8)
		]
		if SystemInfo["CanDownmixAC3"]:
			self.list += [
				(_("Restart audio") + " AC3", config.plugins.AC3LipSync.restartSelection),
				(_("Restart audio delay (in sec)"), config.plugins.AC3LipSync.restartDelay)
			]
		ConfigListScreen.__init__(self, self.list)
		self["config"].list = self.list
		self.skin_path = plugin_path
		self["PluginInfo"] = Label(_("Plugin: %(plugin)s, Version: %(version)s") % dict(plugin=PLUGIN_BASE, version=PLUGIN_VERSION))
		self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Save"))
		self["key_yellow"] = Button("")
		self["key_blue"] = Button("")

		self["setupActions"] = NumberActionMap(["SetupActions", "ColorActions"],
		{
			"save": self.save,
			"cancel": self.cancel,
			"green": self.save,
			"red": self.cancel,
			"ok": self.save,
		}, -2)

	def save(self):
		for x in self.list:
			x[1].save()
		self.close()

	def cancel(self):
		for x in self["config"].list:
			x[1].cancel()
		self.close()
