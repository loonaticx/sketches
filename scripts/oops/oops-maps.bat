:: Oops, I accidentally decided to use a script that modifies every single texture in the resources!

:: And if I try to use a GUI-based git client like GitHub desktop, which has a very bad recursion algorithm,
:: everything will end up freezing!

for %%G IN (3, 3.5, 4, 5, 5.5, 6, 7, 8, 9, 10, 11, 12, 13) do git restore phase_%%G/maps
pause
