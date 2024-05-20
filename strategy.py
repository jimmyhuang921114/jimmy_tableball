import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import sys
from threading import Thread
from . import tableball as table  # Adjust this import based on your file structure
import pygame as pg

class BoxSubscriber(Node):
    def __init__(self, game):
        super().__init__('pygame_node')
        self.subscription = self.create_subscription(Float64MultiArray, 'center_data_coords', self.strategy_callback, 10)
        self.publisher_strategy = self.create_publisher(Float64MultiArray, 'strategy_hitpoint', 10)
        self.game = game

    def strategy_callback(self, msg):
        self.get_logger().info('Received detection results')
        
        # Generate new ball positions and cue ball
        cuex, cuey, ballx_set, bally_set, ballcount = table.generate_balls(8, table.radius)
        
        # Run the main game logic and get the results
        bestscore, bestvx, bestvy, obstacle, x, y = self.game.calculate_strategy(cuex, cuey, ballx_set, bally_set, ballcount)

        # Ensure all values are of type float
        strategy_msg = Float64MultiArray()
        strategy_msg.data = [float(bestscore), float(bestvx), float(bestvy), float(obstacle), float(x), float(y)]
        
        # Publish the strategy data
        self.publisher_strategy.publish(strategy_msg)
        
        self.get_logger().info('Published strategy_hitpoint')

class PygameGame:
    def __init__(self):
        self.running = True
        self.screen = None

    def run(self):
        pg.init()
        self.screen = pg.display.set_mode((1000, 500))
        pg.display.set_caption("Table Tennis")

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            # Fill the screen with a color (e.g., white)
            self.screen.fill((255, 255, 255))

            # Generate and draw balls
            cuex, cuey, ballx_set, bally_set, ballcount = table.generate_balls(8, table.radius)
            table.main(ballx_set, bally_set, ballcount, cuex, cuey)

            # Update the display
            pg.display.flip()

        pg.quit()

    def calculate_strategy(self, cuex, cuey, ballx_set, bally_set, ballcount):
        # This function should encapsulate the logic to calculate the best strategy
        # For now, it just runs the main function and returns some dummy values
        return table.main(ballx_set, bally_set, ballcount, cuex, cuey)

def run_pygame(game):
    game.run()

def main(args=None):
    rclpy.init(args=args)

    # Create the PygameGame instance
    game = PygameGame()

    # Create and run the ROS 2 node
    node = BoxSubscriber(game)
    
    # Run the Pygame game in a separate thread
    pygame_thread = Thread(target=run_pygame, args=(game,))
    pygame_thread.start()
    
    rclpy.spin(node)
    
    # When ROS 2 shuts down, stop the Pygame game
    game.running = False
    pygame_thread.join()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
