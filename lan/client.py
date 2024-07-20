"""
Runs in the background, recieves information from the server, sends it to the game loop
The gameloop will only update on information recieved from the server

First thing that is recieved is the player id and the seed which is stored in the game loop
"""
import socket
import threading

# Need discover logic to find the server to connect to it. Allow user to select the server?
# Once selected join the server and recieve player id and seed
# Once game has started, need to send and recieve information on a given turn