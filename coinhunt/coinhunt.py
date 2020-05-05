from redbot.core import commands
from redbot.core import Config
from .coingame import CoinGame, Direction
import discord
from redbot.core.utils.predicates import ReactionPredicate
import asyncio

EMOJIS = ('❌', '◀️', '🔼', '🔽', '▶️')


class CoinHunt(commands.Cog):
    """A Small Movement Based Coin Collecting Minigame"""
    def __init__(self, bot):
        self.bot = bot

        # Cookie rewards exclusive to Mucski cog, may change the currency
        # You may change the currency and rewards to your liking

        self.cog_loaded = bool(self.bot.get_cog("Mucski"))
        if self.cog_loaded:
            self.config = Config.get_conf(None, cog_name="Mucski", identifier=82838559382)
        else:
            self.config = None

    @commands.command()
    async def coinhunt(self, ctx):
        """
        A Small Minigame where main objective is to collect coins in limited number of moves.

        [@] : Player
        [·] : Visited
        [○] : Coin
        [+] : Power-Ups
        [R] : Reveal-Shard
        """

        game = CoinGame()
        msg = await ctx.send("```\nLoading...\n```")
        try:
            for emoji in EMOJIS:
                await msg.add_reaction(emoji)

        except discord.HTTPException:
            await ctx.send("```/nThere was an error! Please try again./n```")
            return

        while game.stats['moves'] > 0 and game.stats['coins'] != game.stats['max_coins']:
            await msg.edit(content=f"```\n{game.render()}\n```")
            pred = ReactionPredicate.with_emojis(EMOJIS, message=msg, user=ctx.author)
            try:
                await ctx.bot.wait_for("reaction_add", check=pred, timeout=60)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
            emoji = EMOJIS[int(pred.result)]
            if emoji == '❌':
                await msg.clear_reactions()
                await msg.edit(content="```\nGame was cancelled\n```")
                break
            elif emoji == '🔼':
                direction = Direction.up
            elif emoji == '🔽':
                direction = Direction.down
            elif emoji == '▶️':
                direction = Direction.right
            elif emoji == '◀️':
                direction = Direction.left
            game.move_player(direction)
            try:
                await msg.remove_reaction(emoji, ctx.author)
            except discord.HTTPException:
                pass
        score = game.stats['coins'] + game.stats['moves']
        if self.cog_loaded:
            user_coins = await self.config.user(ctx.author).coins()
            user_coins += score
            await self.config.user(ctx.author).coins.set(user_coins)
        if game.stats['moves'] == 0:
            if self.cog_loaded:
                await msg.edit(content=(
                    f"```\nUh oh, Game Over. Your score: {score}\n"
                    f"\nYou get {score} coins for your performance.\n```"
                ))
            else:
                await msg.edit(content=f"```\nUh oh, Game Over. Your score: {score}\n```")

        elif game.stats['coins'] == game.stats['max_coins']:
            if self.cog_loaded:
                await msg.edit(content=(
                    f"```\nCongratulations! You Win. Your score: {score}\n"
                    f"\nYou get {score} coins for beating the game!```"
                ))
            else:
                await msg.edit(content=f"```\nCongratulations! You Win. Your score: {score}\n```")
        await msg.clear_reactions()
