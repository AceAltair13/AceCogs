from redbot.core import commands
from .coingame import CoinGame, Direction
import discord
from redbot.core.utils.predicates import ReactionPredicate
import asyncio

EMOJIS = ('❌', '◀️', '🔼', '🔽', '▶️')


class CoinHunt(commands.Cog):
    """A Small Movement Based Coin Collecting Minigame"""

    @commands.command()
    async def coinhunt(self, ctx):
        """
        A Small Minigame where main objective is to collect coins in limited number of moves.

        [♦] : Player
        [·] : Visited
        [○] : Coin
        [+] : Power-Ups
        [♣] : Reveal-Shard
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
                await ctx.bot.wait_for("reaction_add", check=pred)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                return
            emoji = EMOJIS[pred.result]
            if emoji == '❌':
                await msg.clear_reactions()
                await msg.edit(content="```\nGame was cancelled\n```")
                return
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
        if game.stats['moves'] == 0:
            await msg.edit(content=f"```\nUh oh, Game Over. Your score: {score}\n```")
            await msg.clear_reactions()
            return
        elif game.stats['coins'] == game.stats['max_coins']:
            await msg.edit(content=f"```\nCongratulations! You Win. Your score: {score}\n```")
            await msg.clear_reactions()
            return
