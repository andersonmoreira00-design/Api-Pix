import unittest

from app.models.schemas import PixResponse
from app.routers.pix import _format_pix_response


class PixResponseTest(unittest.TestCase):
    def test_formats_provider_response_without_internal_payload(self):
        provider_response = {
            "success": True,
            "pix_id": "pix-123",
            "cart_id": "cart-123",
            "run_id": "run-123",
            "amount": "0.01",
            "payment_method": "WALLET",
            "receiver": {
                "key": "12345678909",
                "keyType": "CPF",
                "owner": {
                    "name": "Destinatario",
                    "taxIdNumber": "***.456.789-**",
                },
                "account": {
                    "participant": "22896431",
                    "participantName": "PICPAY",
                    "accountNumber": "*****",
                },
            },
            "result": {
                "status": 101,
                "title": "Prontinho! Pix feito.",
                "currency": "BRL",
                "orderId": 123456,
                "callToActions": [
                    {
                        "url": "https://recargapay.com.br/user/history/123456/voucher",
                    }
                ],
                "bannerCarousel": [{"internal": "must not be returned"}],
            },
            "timestamp": "2026-09-12T17:11:51.687948",
            "key_type": "CPF",
            "key_value": "12345678909",
        }

        formatted = _format_pix_response(provider_response)
        response = PixResponse.model_validate(formatted).model_dump(exclude_none=True)

        self.assertTrue(response["success"])
        self.assertEqual(response["transaction"]["status"], "completed")
        self.assertEqual(response["transaction"]["amount"]["formatted"], "R$ 0,01")
        self.assertEqual(response["receiver"]["institution"]["name"], "PICPAY")
        self.assertNotIn("result", response)
        self.assertNotIn("bannerCarousel", str(response))


if __name__ == "__main__":
    unittest.main()
