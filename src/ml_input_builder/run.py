import asyncio

from environs import Env

from src.ml_input_builder.core import MLInputBuilder

async def main():
    env = Env()
    env.read_env()

    ml_input_builder = MLInputBuilder(
        huggingface_token=env.str("HUGGINGFACE_TOKEN")
    )
    # await ml_input_builder.bag_of_words()
    await ml_input_builder.raw()

if __name__ == "__main__":

    asyncio.run(main())