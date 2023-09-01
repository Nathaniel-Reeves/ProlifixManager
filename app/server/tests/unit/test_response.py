# class Test_Response(unittest.TestCase):

#     def test_message_init(self):
#         message = response.Message()
#         self.assertTrue(isinstance(message, response.Message))
#         self.assertEqual(message.alert_heading, None)
#         self.assertEqual(message.message, None)
#         self.assertEqual(message.message_type, response.MessageType.PRIMARY)
#         self.assertEqual(message.icon, "star-fill")
#         self.assertEqual(message.color, "primary")
#         self.assertEqual(message.debug_code, "0")
#         self.assertEqual(message.link, "")

#     def test_change_message_type(self):
#         message = response.Message()

#         # primary => secondary
#         message.set_message_type(response.MessageType.SECONDARY, "1")
#         self.assertEqual(message.message_type, response.MessageType.SECONDARY)
#         self.assertEqual(message.icon, "search")
#         self.assertEqual(message.color, "secondary")
#         self.assertEqual(message.debug_code, "1")

#         # secondary => success
#         message.set_message_type(response.MessageType.SUCCESS, "2")
#         self.assertEqual(message.message_type, response.MessageType.SUCCESS)
#         self.assertEqual(message.icon, "check-circle")
#         self.assertEqual(message.color, "success")
#         self.assertEqual(message.debug_code, "2")

#         # success => danger
#         message.set_message_type(response.MessageType.DANGER, "3")
#         self.assertEqual(message.message_type, response.MessageType.DANGER)
#         self.assertEqual(message.icon, "exclamation-octagon")
#         self.assertEqual(message.color, "danger")
#         self.assertEqual(message.debug_code, "3")

#         # danger => warning
#         message.set_message_type(response.MessageType.WARNING, "4")
#         self.assertEqual(message.message_type, response.MessageType.WARNING)
#         self.assertEqual(message.icon, "exclamation-triangle")
#         self.assertEqual(message.color, "warning")
#         self.assertEqual(message.debug_code, "4")

#         # warning => info
#         message.set_message_type(response.MessageType.INFO, "5")
#         self.assertEqual(message.message_type, response.MessageType.INFO)
#         self.assertEqual(message.icon, "info-circle")
#         self.assertEqual(message.color, "info")
#         self.assertEqual(message.debug_code, "5")

#         # info => light
#         message.set_message_type(response.MessageType.LIGHT, "6")
#         self.assertEqual(message.message_type, response.MessageType.LIGHT)
#         self.assertEqual(message.icon, "star-fill")
#         self.assertEqual(message.color, "light")
#         self.assertEqual(message.debug_code, "6")

#         # light => dark
#         message.set_message_type(response.MessageType.DARK, "7")
#         self.assertEqual(message.message_type, response.MessageType.DARK)
#         self.assertEqual(message.icon, "star-fill")
#         self.assertEqual(message.color, "dark")
#         self.assertEqual(message.debug_code, "7")

#     def test_set_link(self):
#         message = response.Message()
#         message.set_link("http://example.com")
#         self.assertEqual(message.link, "http://example.com")

#     def test_set_icon(self):
#         message = response.Message()
#         message.set_icon(response.MessageType.SUCCESS)
#         self.assertEqual(message.icon, "check-circle")

#     def test_to_json(self):
#         message = response.Message()
#         message.set_message_type(response.MessageType.SUCCESS, "0")
#         self.assertEqual(message.to_json(
#         ), '{"alert_heading": null, "message": null, "message_detail": null, "message_type": "success", "icon": "check-circle", "color": "success", "debug_code": "0", "link": ""}')

#     def test_message_object_to_string(self):
#         message = response.Message()
#         message.set_message_type(response.MessageType.SUCCESS, "0")
#         str_message = str(message)
#         self.assertEqual(
#             str_message, '{"alert_heading": None, "message": None, "message_detail": None, "message_type": "success", "icon": "check-circle", "color": "success", "debug_code": "0", "link": ""}')

#     def test_message_to_dict(self):
#         message = response.Message()
#         message.set_message_type(response.MessageType.SUCCESS, "0")
#         dict_message = dict(message)
#         self.assertTrue(isinstance(dict_message, dict))
#         self.assertEqual(dict_message, {
#             "alert_heading": None,
#             "message": None,
#             "message_detail": None,
#             "message_type": "success",
#             "icon": "check-circle",
#             "color": "success",
#             "debug_code": "0",
#             "link": ""
#         })
