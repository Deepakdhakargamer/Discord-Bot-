import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import sqlite3

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Bot avviato! Connesso come {bot.user}')
    print(f'ID: {bot.user.id}')
    print('------')
    
    try:
        await bot.load_extension('cogs.tickets')
        await bot.load_extension('cogs.orders')
        await bot.load_extension('cogs.reviews')
        await bot.load_extension('cogs.rewards')
        await bot.load_extension('cogs.admin')
        print('Tutti i moduli caricati con successo!')
    except Exception as e:
        print(f'Errore nel caricamento dei moduli: {e}')
    
    try:
        synced = await bot.tree.sync()
        print(f'Sincronizzati {len(synced)} slash commands')
    except Exception as e:
        print(f'Errore nella sincronizzazione: {e}')
    
    await bot.change_presence(activity=discord.Game(name="Server Minecraft Gratuiti | !help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('❌ Comando non trovato! Usa `!help` per vedere i comandi disponibili.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ Non hai i permessi per usare questo comando!')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'❌ Argomento mancante! Usa `!help {ctx.command}` per maggiori info.')
    else:
        await ctx.send(f'❌ Si è verificato un errore: {str(error)}')

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="📋 Comandi Bot - Minecraft Shop",
        description="Ecco tutti i comandi disponibili:",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🎫 Sistema Ticket",
        value="`!ticket` - Apri un ticket di supporto\n`!close` - Chiudi il ticket corrente (Staff)",
        inline=False
    )
    
    embed.add_field(
        name="📦 Sistema Ordini",
        value="`!order <tipo>` - Crea un nuovo ordine\n`!myorders` - Visualizza i tuoi ordini\n`!orderstatus <id>` - Controlla lo stato di un ordine",
        inline=False
    )
    
    embed.add_field(
        name="⭐ Sistema Recensioni",
        value="`!review <voto> <testo>` - Lascia una recensione (1-5 stelle)\n`!reviews` - Visualizza tutte le recensioni",
        inline=False
    )
    
    embed.add_field(
        name="💎 Sistema Punti/Ricompense",
        value="`!points [@utente]` - Visualizza i tuoi punti\n`!rewards` - Vedi ricompense disponibili\n`!leaderboard` - Classifica utenti\n`!daily` - Ricompensa giornaliera\n`!history` - Cronologia punti",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Admin (Solo Staff)",
        value="`!setorder <id> <stato>` - Aggiorna stato ordine\n`!stats` - Statistiche del server\n`!announce <messaggio>` - Invia annuncio\n`!addpoints <utente> <punti> <motivo>` - Aggiungi punti\n`!removepoints <utente> <punti> <motivo>` - Rimuovi punti",
        inline=False
    )
    
    embed.set_footer(text="Bot creato per lo shop di server Minecraft")
    await ctx.send(embed=embed)

os.getenv('DISCORD_TOKEN')