import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, String
import tableball
import paygame
import sys
from threading import Thread


class BoxSubscriber(Node):
    def __init__(self):
        super().__init__('pygame_node')
        self.subscription_coords = self.create_subscription(Float64MultiArray, 'center_data_coords',10)
    
    def coords_callback(self, msg):
        # 在這裡處理從 'center_data_coords' 主題接收到的資料
        coords_data = msg.data
        # 根據您的遊戲邏輯，更新遊戲畫面或執行其他操作
                                                             self.coords_callback, 10)
    #     self.subscription_labels = self.create_subscription(String, 'center_data_labels', self.labels_callback, 10)
    #     self.coords_data = []
    #     self.labels_data = []
    #     self.label_order = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'white']
    #     print('BoxSubscriber has been started and is subscribing.')

    # def coords_callback(self, msg):
    #     self.coords_data = msg.data
    #     print(msg.data[0])
    #     # 重置标签数据以等待新的完整数据集
    #     self.labels_data = []

    # def labels_callback(self, msg):
    #     if msg.data in self.label_order:
    #         self.labels_data.append(msg.data)
    #         if len(self.coords_data) // 2 == len(self.labels_data):
    #             self.display_data()

    # def display_data(self):
    #     if self.coords_data and self.labels_data:
    #         combined_data = []
    #         for label in self.label_order:
    #             if label in self.labels_data:
    #                 index = self.labels_data.index(label)
    #                 x = self.coords_data[index * 2]
    #                 y = self.coords_data[index * 2 + 1]
    #                 combined_data.append(f'{label}, ({x:.2f}, {y:.2f})')
    #         print('\n'.join(combined_data))
    #         # Reset data after displaying
    #         self.coords_data = []
    #         self.labels_data = []


class TableBallNode(Node):
    def __init__(self):
        super().__init__('tableball_node')
        self.initialize_pygame()
        self.timer = self.create_timer(0.1, self.update_game)  # 10 Hz game update

    def initialize_pygame(self):
        tableball.init()
        self.width, self.height = 1000, 500
        self.screen = tableball.display.set_mode((self.width, self.height))
        tableball.display.set_caption("Table Ball")

    def update_game(self):
        for event in tableball.event.get():
            if event.type == tableball.QUIT:
                tableball.quit()
                sys.exit()
            # Add more event handling here

        # Update game logic here
        self.screen.fill((255, 255, 255))  # Fill screen with white
        tableball.display.flip()  # Update display


def start_ros_node(node):
    rclpy.spin(node)


def main(args=None):
    rclpy.init(args=args)
    box_subscriber_node = BoxSubscriber()
    table_ball_node = TableBallNode()
    ros_thread1 = Thread(target=start_ros_node, args=(box_subscriber_node,))
    ros_thread2 = Thread(target=start_ros_node, args=(table_ball_node,))
    ros_thread1.start()
    ros_thread2.start()
    ros_thread1.join()
    ros_thread2.join()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
