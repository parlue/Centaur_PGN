
import asyncio
import chess
import chess.engine

async def main() -> None:
	transport, engine = await chess.engine.popen_uci(r"/home/pi/v2/engines/montreux")
	engine.configure("level = 5 min/game")
	engine.configure("ponder = True")

	board = chess.Board()
	while not board.is_game_over():
		result = await engine.play(board, chess.engine.Limit(time=15))
		print(result)
		board.push(result.move)

	await engine.quit()

asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
asyncio.run(main())