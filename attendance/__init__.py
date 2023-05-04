from .attendance import Attendance

def setup(bot):
    cog = Attendance(bot)
    await bot.add_cog(cog)