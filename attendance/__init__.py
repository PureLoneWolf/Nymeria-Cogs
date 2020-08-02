from .attendance import Attendance

def setup(bot):
    cog = Attendance(bot)
    bot.add_cog(cog)