from rest_framework import serializers
from .models import CartItem, Cart, Booking, Ticket

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'event', 'offer', 'quantity', 'total_price']
        read_only_fields = ['total_price']

    # Valide que la quantité soit supérieure à zéro
    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("La quantité doit être supérieure à zéro.")
        return data
    
    # Crée un nouvel article dans le panier en calculant le prix total en fonction de la quantité
    def create(self, validated_data):
        event = validated_data['event']
        offer = validated_data['offer']
        quantity = validated_data['quantity']

        if offer == "solo":
            total_price = event.price_solo * quantity
        elif offer == "duo":
            total_price = event.price_duo * quantity
        elif offer == "family":
            total_price = event.price_family * quantity
        else:
            raise serializers.ValidationError("L'offre n'est pas valide.")

        # Créer l'article avec le prix total calculé
        cart_item = CartItem.objects.create(
            cart=validated_data['cart'],
            event=event,
            offer=offer,
            quantity=quantity,
            total_price=total_price
        )
        return cart_item
    

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
        read_only_fields = ['user', 'created_at']

    # Retourner tous les articles dans le panier
    def get_items(self):
        return CartItem.objects.filter(cart=self.instance)

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'total_price', 'booking_date']
        read_only_fields = ['user', 'total_price', 'booking_date']

    # Crée une réservation en calculant le prix total du panier et en générant les billets
    def create(self, validated_data):
        cart = Cart.objects.get(user=self.context['request'].user)
        total_price = sum(item.total_price for item in cart.items.all())

        # Créer la réservation
        booking = Booking.objects.create(user=self.context['request'].user, total_price=total_price)

        # Créer les billets pour chaque article dans le panier
        for item in cart.items.all():
            Ticket.objects.create(
                booking=booking,
                event=item.event,
                offer=item.offer,
            )

        # Vider le panier après validation
        cart.items.all().delete()

        return booking    

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'booking', 'event', 'offer', 'qr_code', 'issued_at']
        read_only_fields = ['qr_code', 'issued_at']