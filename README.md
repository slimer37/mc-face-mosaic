# Crafatar Mosaic
Simple Python program that uses Crafatar to make a grid of player heads.

I made this to generate icons for a Minecraft server.

1. Provide an input `names.txt` file in the following format:

    ```
    Grian
    Notch
    stampylongnose
    Sethbling
    jeb_
    DanTDM
    MumboJumbo
    Grumm
    AntVenom
    ```

    > You can exclude lines with `#` at the beginning of the line.
    > Names with errors get their spot in the grid replaced with this placeholder:
    >
    > <img src="src/placeholder/missing-face.png" alt="Placeholder" style="width:100px; image-rendering: pixelated;"/>

1. Run `python src/main.py` and find the mosaic in `output/mosaic@xxx.png`. 

    ![Sample Mosaic](assets/sample.png)