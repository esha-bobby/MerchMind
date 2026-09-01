'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';

interface Product {
  id: string;
  title: string;
  description: string;
  category?: string;
  price?: number;
  colors?: string[];
  sizes?: string[];
  material?: string;
  reviews?: number;
  return_policy?: string;
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/products');
        if (!response.ok) throw new Error('Failed to fetch products');
        const data = await response.json();
        setProducts(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error loading products');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const categories = useMemo(
    () => ['all', ...new Set(products.map((product) => product.category).filter(Boolean) as string[])],
    [products]
  );

  const filteredProducts = useMemo(() => {
    const normalizedQuery = searchQuery.trim().toLowerCase();

    return products.filter((product) => {
      const matchesSearch =
        normalizedQuery.length === 0 ||
        product.title.toLowerCase().includes(normalizedQuery) ||
        product.description.toLowerCase().includes(normalizedQuery);

      const matchesCategory =
        selectedCategory === 'all' || product.category === selectedCategory;

      return matchesSearch && matchesCategory;
    });
  }, [products, searchQuery, selectedCategory]);

  return (
    <div className="min-h-screen p-6 md:p-12">
      <header className="mb-12 text-center">
        <h1 className="text-5xl font-bold text-accent mb-2">MerchMind</h1>
        <p className="text-lg text-gray-700">
          Check if your product descriptions are ready for AI shopping assistants
        </p>
      </header>

      {loading && (
        <div className="text-center py-12">
          <p className="text-gray-600 text-lg">Loading your products...</p>
        </div>
      )}

      {error && (
        <div className="max-w-2xl mx-auto mb-8 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-700">⚠️ {error}</p>
          <p className="text-sm text-red-600 mt-2">
            Make sure the backend is running on http://localhost:8000
          </p>
        </div>
      )}

      {!loading && products.length > 0 && (
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
              <p className="text-sm text-gray-500">Total products</p>
              <p className="text-3xl font-bold text-gray-900">{products.length}</p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
              <p className="text-sm text-gray-500">Categories</p>
              <p className="text-3xl font-bold text-gray-900">{categories.length - 1}</p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
              <p className="text-sm text-gray-500">Visible products</p>
              <p className="text-3xl font-bold text-gray-900">{filteredProducts.length}</p>
            </div>
          </div>

          <div className="mb-8 flex flex-col md:flex-row gap-3">
            <input
              type="text"
              placeholder="Search product titles or descriptions"
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
              className="flex-1 border border-gray-200 rounded-lg px-4 py-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-accent/20"
            />

            <select
              value={selectedCategory}
              onChange={(event) => setSelectedCategory(event.target.value)}
              className="border border-gray-200 rounded-lg px-4 py-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-accent/20"
            >
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category === 'all' ? 'All categories' : category}
                </option>
              ))}
            </select>
          </div>

          {filteredProducts.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredProducts.map((product) => (
                <Link key={product.id} href={`/audit/${product.id}`}>
                  <div className="bg-white rounded-xl shadow-sm hover:shadow-lg transition-shadow p-6 cursor-pointer border border-gray-100 hover:border-accent/30">
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="font-semibold text-lg text-gray-900 flex-1">
                        {product.title}
                      </h3>
                      <span className="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded">
                        {product.category}
                      </span>
                    </div>

                    <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                      {product.description}
                    </p>

                    <div className="flex items-baseline gap-2 mb-4">
                      {product.price && (
                        <span className="text-2xl font-bold text-accent">
                          ${product.price.toFixed(2)}
                        </span>
                      )}
                    </div>

                    <div className="flex flex-wrap gap-2 mb-4">
                      {product.colors && product.colors.length > 0 && (
                        <span className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded">
                          {product.colors.length} color{product.colors.length > 1 ? 's' : ''}
                        </span>
                      )}
                      {product.sizes && product.sizes.length > 0 && (
                        <span className="text-xs bg-purple-50 text-purple-700 px-2 py-1 rounded">
                          {product.sizes.length} size{product.sizes.length > 1 ? 's' : ''}
                        </span>
                      )}
                    </div>

                    <button className="w-full bg-accent text-white py-2 rounded-lg font-medium hover:bg-opacity-90 transition-all">
                      Audit This Product →
                    </button>
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 bg-white rounded-xl border border-gray-100 shadow-sm">
              <p className="text-lg text-gray-700">No products match your current filters.</p>
              <button
                onClick={() => {
                  setSearchQuery('');
                  setSelectedCategory('all');
                }}
                className="mt-4 bg-accent text-white px-4 py-2 rounded-lg font-medium"
              >
                Clear filters
              </button>
            </div>
          )}
        </div>
      )}

      {!loading && products.length === 0 && !error && (
        <div className="text-center py-12">
          <p className="text-gray-600">No products found</p>
        </div>
      )}
    </div>
  );
}
