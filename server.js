const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Read products from JSON file created by Python scraper
function readProductsFromFile() {
    try {
        const filePath = path.join(__dirname, 'products.json');
        const data = fs.readFileSync(filePath, 'utf8');
        const parsed = JSON.parse(data);
        return parsed;
    } catch (error) {
        console.error('❌ Error reading products.json:', error.message);
        console.log('💡 Make sure to run: python scraper.py');
        return null;
    }
}

// Root endpoint - API documentation
app.get('/', (req, res) => {
    res.json({
        name: 'TrendTracker API',
        version: '3.0',
        status: 'running',
        endpoints: {
            'GET /': 'This documentation',
            'GET /api/trending': 'Get all trending products',
            'GET /api/trending/amazon': 'Get Amazon products only',
            'GET /api/trending/producthunt': 'Get Product Hunt products only',
            'GET /api/health': 'Health check',
            'GET /api/stats': 'Get statistics'
        },
        note: 'Data is updated by running: python scraper.py'
    });
});

// Health check
app.get('/api/health', (req, res) => {
    const data = readProductsFromFile();
    
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        dataAvailable: data !== null,
        productCount: data ? data.count : 0
    });
});

// Statistics endpoint
app.get('/api/stats', (req, res) => {
    const data = readProductsFromFile();
    
    if (!data) {
        return res.status(404).json({
            success: false,
            error: 'No data available. Run: python scraper.py'
        });
    }
    
    const platforms = {};
    data.products.forEach(product => {
        platforms[product.platform] = (platforms[product.platform] || 0) + 1;
    });
    
    res.json({
        success: true,
        totalProducts: data.count,
        platforms: platforms,
        lastUpdate: data.lastUpdate
    });
});

// Get all trending products
app.get('/api/trending', (req, res) => {
    const data = readProductsFromFile();
    
    if (!data) {
        return res.status(404).json({
            success: false,
            error: 'No data available',
            message: 'Please run: python scraper.py first'
        });
    }
    
    res.json({
        success: true,
        count: data.count,
        products: data.products,
        lastUpdate: data.lastUpdate
    });
});

// Get Amazon products only
app.get('/api/trending/amazon', (req, res) => {
    const data = readProductsFromFile();
    
    if (!data) {
        return res.status(404).json({
            success: false,
            error: 'No data available'
        });
    }
    
    const amazonProducts = data.products.filter(p => p.platform === 'Amazon');
    
    res.json({
        success: true,
        count: amazonProducts.length,
        products: amazonProducts,
        lastUpdate: data.lastUpdate
    });
});

// Get Product Hunt products only
app.get('/api/trending/producthunt', (req, res) => {
    const data = readProductsFromFile();
    
    if (!data) {
        return res.status(404).json({
            success: false,
            error: 'No data available'
        });
    }
    
    const phProducts = data.products.filter(p => p.platform === 'Product Hunt');
    
    res.json({
        success: true,
        count: phProducts.length,
        products: phProducts,
        lastUpdate: data.lastUpdate
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        success: false,
        error: 'Endpoint not found',
        availableEndpoints: [
            '/api/trending',
            '/api/trending/amazon',
            '/api/trending/producthunt',
            '/api/health',
            '/api/stats'
        ]
    });
});

// Start server
app.listen(PORT, () => {
    console.log('\n' + '='.repeat(60));
    console.log('🚀 TrendTracker API v3.0');
    console.log('='.repeat(60));
    console.log(`📡 Server running: http://localhost:${PORT}`);
    console.log(`📖 API Docs: http://localhost:${PORT}/`);
    console.log(`🔥 Trending: http://localhost:${PORT}/api/trending`);
    console.log('='.repeat(60));
    console.log('\n💡 To update data: python scraper.py');
    console.log('='.repeat(60) + '\n');
    
    // Check if products.json exists
    if (!fs.existsSync(path.join(__dirname, 'products.json'))) {
        console.log('⚠️  WARNING: products.json not found!');
        console.log('   Run: python scraper.py\n');
    } else {
        console.log('✅ products.json found\n');
    }
});

// Export for testing
module.exports = app;