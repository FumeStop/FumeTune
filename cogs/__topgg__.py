from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import tasks, commands

if TYPE_CHECKING:
    from bot import FumeTune


class TopGG(commands.Cog):
    def __init__(self, bot: FumeTune):
        self.bot: FumeTune = bot

    @tasks.loop(minutes=15)
    async def _update_stats(self):
        try:
            await self.bot.topggpy.post_guild_count(
                guild_count=len(self.bot.guilds), shard_count=len(self.bot.shards)
            )
            self.bot.log.info(
                f"Posted server count ({self.bot.topggpy.guild_count})"
            )

        except Exception as e:
            self.bot.log.error(f"Failed to post server count", exc_info=e)

    @commands.Cog.listener()
    async def on_ready(self):
        self._update_stats.start()
        self.bot.log.info("Top.gg webhook is ready")


async def setup(bot):
    await bot.add_cog(TopGG(bot))
