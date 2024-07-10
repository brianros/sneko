# import uasyncio # type: ignore
# from rotary_encoder import RotaryEncoder

# async def main():
#     # Initialize the rotary encoder with GPIO pins
#     encoder = RotaryEncoder(clk_pin=25, dt_pin=26, sw_pin=27)
    
#     # Start the encoder
#     encoder.start()
    
#     # Run your main program logic
#     while True:
#         for a in range(10):
#             await asyncio.sleep(1)
#             print(encoder.get_counter())
#         await asyncio.sleep(10)
#         encoder.reset_counter()

# # Run the main function
# asyncio.run(main())
