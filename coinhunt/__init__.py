from .coinhunt import CoinHunt


def setup(bot):
    bot.add_cog(CoinHunt(bot))
