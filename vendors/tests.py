from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Vendor, PurchaseOrder
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class VendorTests(APITestCase):

    def test_create_vendor(self):
        url = reverse('vendor-list')
        data = {
            'name': 'Vendor Name',
            'contact_details': 'Contact Details',
            'address': 'Vendor Address',
            'vendor_code': 'UNIQUECODE'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, 'Vendor Name')

    def test_list_vendors(self):
        Vendor.objects.create(name='Vendor 1', contact_details='Contact 1', address='Address 1', vendor_code='CODE1')
        Vendor.objects.create(name='Vendor 2', contact_details='Contact 2', address='Address 2', vendor_code='CODE2')
        url = reverse('vendor-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_vendor(self):
        vendor = Vendor.objects.create(name='Vendor Name', contact_details='Contact Details', address='Vendor Address', vendor_code='UNIQUECODE')
        url = reverse('vendor-detail', args=[vendor.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Vendor Name')

    def test_update_vendor(self):
        vendor = Vendor.objects.create(name='Vendor Name', contact_details='Contact Details', address='Vendor Address', vendor_code='UNIQUECODE')
        url = reverse('vendor-detail', args=[vendor.id])
        data = {
            'name': 'Updated Vendor Name',
            'contact_details': 'Updated Contact Details',
            'address': 'Updated Vendor Address',
            'vendor_code': 'UPDATEDCODE'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vendor.refresh_from_db()
        self.assertEqual(vendor.name, 'Updated Vendor Name')

    def test_delete_vendor(self):
        vendor = Vendor.objects.create(name='Vendor Name', contact_details='Contact Details', address='Vendor Address', vendor_code='UNIQUECODE')
        url = reverse('vendor-detail', args=[vendor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

class PurchaseOrderTests(APITestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(name='Vendor Name', contact_details='Contact Details', address='Vendor Address', vendor_code='UNIQUECODE')

    def test_create_purchase_order(self):
        url = reverse('purchaseorder-list')
        data = {
            'po_number': 'PO12345',
            'vendor': self.vendor.id,
            'order_date': '2024-01-01T12:00:00Z',
            'delivery_date': '2024-01-10T12:00:00Z',
            'items': {'item1': 'description', 'item2': 'description'},
            'quantity': 100,
            'status': 'pending',
            'issue_date': '2024-01-01T12:00:00Z'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)
        self.assertEqual(PurchaseOrder.objects.get().po_number, 'PO12345')

    def test_list_purchase_orders(self):
        PurchaseOrder.objects.create(po_number='PO12345', vendor=self.vendor, order_date='2024-01-01T12:00:00Z', delivery_date='2024-01-10T12:00:00Z', items={'item1': 'description', 'item2': 'description'}, quantity=100, status='pending', issue_date='2024-01-01T12:00:00Z')
        url = reverse('purchaseorder-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_purchase_order(self):
        purchase_order = PurchaseOrder.objects.create(po_number='PO12345', vendor=self.vendor, order_date='2024-01-01T12:00:00Z', delivery_date='2024-01-10T12:00:00Z', items={'item1': 'description', 'item2': 'description'}, quantity=100, status='pending', issue_date='2024-01-01T12:00:00Z')
        url = reverse('purchaseorder-detail', args=[purchase_order.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], 'PO12345')

    def test_update_purchase_order(self):
        purchase_order = PurchaseOrder.objects.create(po_number='PO12345', vendor=self.vendor, order_date='2024-01-01T12:00:00Z', delivery_date='2024-01-10T12:00:00Z', items={'item1': 'description', 'item2': 'description'}, quantity=100, status='pending', issue_date='2024-01-01T12:00:00Z')
        url = reverse('purchaseorder-detail', args=[purchase_order.id])
        data = {
            'po_number': 'PO12345',
            'vendor': self.vendor.id,
            'order_date': '2024-01-01T12:00:00Z',
            'delivery_date': '2024-01-10T12:00:00Z',
            'items': {'item1': 'updated description', 'item2': 'updated description'},
            'quantity': 150,
            'status': 'completed',
            'quality_rating': 4.5,
            'issue_date': '2024-01-01T12:00:00Z',
            'acknowledgment_date': '2024-01-02T12:00:00Z'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        purchase_order.refresh_from_db()
        self.assertEqual(purchase_order.quantity, 150)
        self.assertEqual(purchase_order.status, 'completed')
        self.assertEqual(purchase_order.quality_rating, 4.5)

    def test_delete_purchase_order(self):
        purchase_order = PurchaseOrder.objects.create(po_number='PO12345', vendor=self.vendor, order_date='2024-01-01T12:00:00Z', delivery_date='2024-01-10T12:00:00Z', items={'item1': 'description', 'item2': 'description'}, quantity=100, status='pending', issue_date='2024-01-01T12:00:00Z')
        url = reverse('purchaseorder-detail', args=[purchase_order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_acknowledge_purchase_order(self):
        purchase_order = PurchaseOrder.objects.create(po_number='PO12345', vendor=self.vendor, order_date='2024-01-01T12:00:00Z', delivery_date='2024-01-10T12:00:00Z', items={'item1': 'description', 'item2': 'description'}, quantity=100, status='pending', issue_date='2024-01-01T12:00:00Z')
        url = reverse('purchaseorder-acknowledge', args=[purchase_order.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        purchase_order.refresh_from_db()
        self.assertIsNotNone(purchase_order.acknowledgment_date)

class VendorPerformanceTests(APITestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(name='Vendor Name', contact_details='Contact Details', address='Vendor Address', vendor_code='UNIQUECODE')

    def test_vendor_performance_metrics(self):
        aware_date = make_aware(datetime.now())
        PurchaseOrder.objects.create(po_number='PO12345', vendor=self.vendor, order_date=aware_date, delivery_date=aware_date + timedelta(days=10), items={'item1': 'description', 'item2': 'description'}, quantity=100, status='completed', issue_date=aware_date, acknowledgment_date=aware_date + timedelta(hours=1), quality_rating=4.5)
        PurchaseOrder.objects.create(po_number='PO12346', vendor=self.vendor, order_date=aware_date, delivery_date=aware_date + timedelta(days=5), items={'item1': 'description', 'item2': 'description'}, quantity=200, status='completed', issue_date=aware_date, acknowledgment_date=aware_date + timedelta(hours=2), quality_rating=5.0)
        
        url = reverse('vendor-performance', args=[self.vendor.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('on_time_delivery_rate', response.data)
        self.assertIn('quality_rating_avg', response.data)
        self.assertIn('average_response_time', response.data)
        self.assertIn('fulfillment_rate', response.data)
