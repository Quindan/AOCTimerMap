# AOCTimerMap

### Features : 
- permet de marquer les boss et les ressources (et ce que vous voulez) sur la carte, vous pouvez mettre un timer et le respawn time, et le type
- Tout les pins sont mis en base de donnée, et tout le monde récupere tout les marqueurs et tout les timers ( mis à jour toutes minutes en direct)
sous forme de pin de loin, et de petit carré avec le timer quand c'est zoom; avec le pti icon
- on peut clic pour R (reset le timer), ou M (annoncé que c'est missing)
marqueur rouge pendant le temps où c'est en cooldown. Si tu récupere la resource ou voit le boss mourir, tu clic et reset le timer, il sera rouge pendant 30m ( ou le temps du cooldown réglé) puis reviendra à bleu. (passe jaune pendant le temps de cd si il est marqué missing)
- si l'icone du type existe dans le project, ça met un pti icon, (liste des icons pour l'instant: https://github.com/Quindan/AOCTimerMap/tree/main/src/icons)

### Utilisation : 
- Je coupe un wipping willow legendaire, je vais sur la map, je zoom bien et je clic dessus, je tape 'wipping legendaire' ou peu importe, tape le temps (je crois que c'est 4heure, alors tu tape '4h'), et le type (j'ai mis 'ww' pour wipping willow,mais il y a 'wood' qui existe si tu veux pas te prendre la tete).
- Le point apparait sur la carte pour tout le monde dans la minute, reste rouge pendant 4h.
4h après, le pin repasse bleu. Je reprend le willow. Je clic sur le pin, tape 'r' pour reset. Il redevient rouge pour tout le monde. si les gens zoom, ils voyent le timer précis.


# Install
Install docker and makefile 

```
make install
make run
```

# Known issue
- install : Need to fiddle with right for db/ or src/db/
- pin: cancel pin creation don't work properly
- pin: delay for pin getting the right color, will move to icon instead of le css rotation
- icons: missing a lot of icons, maybe directly taken from codex instead of copying, but would lose the ease to use
