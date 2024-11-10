import React, { useState } from 'react';
import { TextField, Button, Container, Typography } from '@mui/material';
import axios from 'axios';

function ProductForm({ onProductAdded }) {
    const [product, setProduct] = useState({
        name: '',
        description: '',
        unit_price: '',
        stock: ''
    });

    const handleChange = (e) => {
        setProduct({ ...product, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://127.0.0.1:5000/api/products', product);
            onProductAdded();  // Listeyi güncellemek için
            setProduct({ name: '', description: '', unit_price: '', stock: '' });
        } catch (error) {
            console.error("Ürün eklenirken hata oluştu:", error);
        }
    };

    return (
        <Container maxWidth="sm">
            <Typography variant="h5" gutterBottom>Ürün Ekle</Typography>
            <form onSubmit={handleSubmit}>
                <TextField
                    label="Ürün Adı"
                    name="name"
                    value={product.name}
                    onChange={handleChange}
                    fullWidth
                    margin="normal"
                    required
                />
                <TextField
                    label="Açıklama"
                    name="description"
                    value={product.description}
                    onChange={handleChange}
                    fullWidth
                    margin="normal"
                />
                <TextField
                    label="Birim Fiyatı"
                    name="unit_price"
                    type="number"
                    value={product.unit_price}
                    onChange={handleChange}
                    fullWidth
                    margin="normal"
                    required
                />
                <TextField
                    label="Stok"
                    name="stock"
                    type="number"
                    value={product.stock}
                    onChange={handleChange}
                    fullWidth
                    margin="normal"
                    required
                />
                <Button variant="contained" color="primary" type="submit">Ürün Ekle</Button>
            </form>
        </Container>
    );
}

export default ProductForm;
