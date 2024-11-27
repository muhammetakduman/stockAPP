import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
    Container,
    Typography,
    List,
    ListItem,
    ListItemText,
    Button,
    TextField,
} from '@mui/material';

function ProductList() {
    const [products, setProducts] = useState([]);
    const [editingProduct, setEditingProduct] = useState(null);
    const [newStock, setNewStock] = useState('');

    const fetchProducts = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/products');
            setProducts(response.data.products);
        } catch (error) {
            console.error("Ürünler alınırken hata oluştu:", error);
        }
    };

    useEffect(() => {
        fetchProducts();
    }, []);

    // Stok güncelleme işlemi
    const updateStock = async (id) => {
        try {
            await axios.put(`http://127.0.0.1:5000/api/products/${id}`, { stock: newStock });
            setNewStock(''); // Input alanını sıfırla
            setEditingProduct(null); // Düzenleme modundan çık
            fetchProducts(); // Ürün listesini güncelle
        } catch (error) {
            console.error("Stok güncellenirken hata oluştu:", error);
        }
    };

    // Ürünü silme işlemi
    const deleteProduct = async (id) => {
        try {
            await axios.delete(`http://127.0.0.1:5000/api/products/${id}`);
            fetchProducts(); // Ürün listesini güncelle
        } catch (error) {
            console.error("Ürün silinirken hata oluştu:", error);
        }
    };

    return (
        <Container maxWidth="sm">
            <Typography variant="h5" gutterBottom>Ürün Listesi</Typography>
            <List>
                {products.map((product) => (
                    <ListItem key={product.id} divider>
                        <ListItemText
                            primary={product.name}
                            secondary={`Açıklama: ${product.description}, Fiyat: ${product.unit_price} TL, Stok: ${product.stock}, Toplam Tutar: ${product.stock * product.unit_price} TL`}
                        />
                        {editingProduct === product.id ? (
                            <>
                                <TextField
                                    type="number"
                                    size="small"
                                    value={newStock}
                                    onChange={(e) => setNewStock(e.target.value)}
                                    placeholder="Yeni stok miktarı"
                                />
                                <Button onClick={() => updateStock(product.id)} color="primary">Kaydet</Button>
                                <Button onClick={() => setEditingProduct(null)} color="secondary">İptal</Button>
                            </>
                        ) : (
                            <>
                                <Button onClick={() => setEditingProduct(product.id)} color="primary">Stok Güncelle</Button>
                                <Button onClick={() => deleteProduct(product.id)} color="error">Sil</Button>
                            </>
                        )}
                    </ListItem>
                ))}
            </List>
        </Container>
    );
}

export default ProductList;
