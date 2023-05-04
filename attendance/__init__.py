from .attendance import Attendance

async def setup(bot):
    cog = Attendance(bot)
    await bot.add_cog(cog)