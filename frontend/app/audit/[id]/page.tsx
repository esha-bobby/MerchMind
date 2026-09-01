'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

interface FieldStatus {
  field_name: string;
  present: boolean;
  quality: string;
  feedback?: string;
}

interface AuditResult {
  product_id: string;
  product_title: string;
  readiness_score: number;
  field_checks: FieldStatus[];
  description_quality: string;
  missing_critical_fields: string[];
  recommendations: string[];
  summary: string;
}

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

const getScoreColor = (score: number) => {
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  if (score >= 40) return 'text-orange-600';
  return 'text-red-600';
};

const getScoreBg = (score: number) => {
  if (score >= 80) return 'bg-green-50 border-green-200';
  if (score >= 60) return 'bg-yellow-50 border-yellow-200';
  if (score >= 40) return 'bg-orange-50 border-orange-200';
  return 'bg-red-50 border-red-200';
};

const getScoreEmoji = (score: number) => {
  if (score >= 80) return '✓';
  if (score >= 60) return '◐';
  if (score >= 40) return '✕';
  return '✗';
};

export default function AuditPage() {
  const params = useParams();
  const productId = params.id as string;

  const [product, setProduct] = useState<Product | null>(null);
  const [auditResult, setAuditResult] = useState<AuditResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch product
        const productsResponse = await fetch('http://localhost:8000/api/products');
        if (!productsResponse.ok) throw new Error('Failed to fetch products');
        const products: Product[] = await productsResponse.json();
        const foundProduct = products.find((p) => p.id === productId);
        
        if (!foundProduct) throw new Error('Product not found');
        setProduct(foundProduct);

        // Fetch audit result
        const auditResponse = await fetch('http://localhost:8000/api/audit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(foundProduct),
        });

        if (!auditResponse.ok) throw new Error('Failed to audit product');
        const audit: AuditResult = await auditResponse.json();
        setAuditResult(audit);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error loading data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [productId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center p-6">
        <p className="text-lg text-gray-600">Auditing your product...</p>
      </div>
    );
  }

  if (error || !product || !auditResult) {
    return (
      <div className="min-h-screen p-6 md:p-12">
        <Link href="/" className="text-accent hover:underline mb-6 inline-block">
          ← Back to Products
        </Link>
        <div className="max-w-2xl mx-auto p-6 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-700 font-medium">Error</p>
          <p className="text-red-600 mt-2">{error || 'Could not load product data'}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6 md:p-12">
      <Link href="/" className="text-accent hover:underline mb-8 inline-block font-medium">
        ← Back to Products
      </Link>

      <div className="max-w-4xl mx-auto">
        {/* Product Info */}
        <div className="bg-white rounded-xl shadow-sm p-8 mb-8 border border-gray-100">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.title}</h1>
          <p className="text-gray-600 text-lg mb-6">{product.description}</p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {product.price && (
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide">Price</p>
                <p className="text-2xl font-bold text-accent">${product.price.toFixed(2)}</p>
              </div>
            )}
            {product.category && (
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide">Category</p>
                <p className="text-lg font-semibold text-gray-900">{product.category}</p>
              </div>
            )}
            {product.colors && product.colors.length > 0 && (
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide">Colors</p>
                <p className="text-sm text-gray-700">{product.colors.join(', ')}</p>
              </div>
            )}
            {product.sizes && product.sizes.length > 0 && (
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide">Sizes</p>
                <p className="text-sm text-gray-700">{product.sizes.join(', ')}</p>
              </div>
            )}
          </div>
        </div>

        {/* Score Card */}
        <div
          className={`bg-white rounded-xl shadow-sm p-8 mb-8 border-2 ${getScoreBg(
            auditResult.readiness_score
          )}`}
        >
          <div className="flex items-start gap-6">
            <div className="flex-1">
              <p className="text-sm text-gray-600 uppercase tracking-wide mb-2">
                AI Readiness Score
              </p>
              <p className={`text-6xl font-bold ${getScoreColor(auditResult.readiness_score)}`}>
                {Math.round(auditResult.readiness_score)}
              </p>
              <p className="text-gray-700 mt-4 text-lg">{auditResult.summary}</p>
            </div>
            <div className="text-right">
              <p className={`text-8xl font-bold opacity-20 ${getScoreColor(auditResult.readiness_score)}`}>
                {getScoreEmoji(auditResult.readiness_score)}
              </p>
            </div>
          </div>
        </div>

        {/* Description Quality */}
        <div className="bg-white rounded-xl shadow-sm p-8 mb-8 border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Description Quality</h2>

          <div className="mb-6">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-3xl">
                {auditResult.description_quality === 'clear'
                  ? '✓'
                  : auditResult.description_quality === 'vague'
                  ? '◐'
                  : '✕'}
              </span>
              <span className="text-lg font-semibold text-gray-900 capitalize">
                {auditResult.description_quality}
              </span>
            </div>
            <p className="text-gray-600">
              {auditResult.description_quality === 'clear'
                ? 'Your description is clear and specific, perfect for AI assistants.'
                : auditResult.description_quality === 'vague'
                ? 'Your description uses vague language. Include specific details like materials, dimensions, and features.'
                : 'Your description is missing or very incomplete.'}
            </p>
          </div>
        </div>

        {/* Field Checks */}
        <div className="bg-white rounded-xl shadow-sm p-8 mb-8 border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Field Details</h2>

          <div className="space-y-4">
            {auditResult.field_checks.map((field) => (
              <div
                key={field.field_name}
                className="p-4 border border-gray-200 rounded-lg bg-gray-50"
              >
                <div className="flex items-start gap-3">
                  <span className="text-2xl mt-1">
                    {field.quality === 'good' ? '✓' : field.quality === 'vague' ? '◐' : '✕'}
                  </span>
                  <div className="flex-1">
                    <p className="font-semibold text-gray-900 capitalize">{field.field_name}</p>
                    {field.feedback && (
                      <p className="text-sm text-gray-600 mt-1">{field.feedback}</p>
                    )}
                    <p className="text-xs text-gray-500 mt-2">
                      {field.quality === 'good' ? 'Present' : field.quality === 'vague' ? 'Present but unclear' : 'Missing'}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recommendations */}
        <div className="bg-white rounded-xl shadow-sm p-8 border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Recommendations</h2>

          <div className="space-y-3">
            {auditResult.recommendations.map((rec, idx) => (
              <div key={idx} className="flex gap-3 p-3 bg-warm/20 rounded-lg border border-warm">
                <span className="text-lg">→</span>
                <p className="text-gray-800">{rec}</p>
              </div>
            ))}
          </div>

          <div className="mt-8 pt-6 border-t border-gray-200">
            <Link
              href="/"
              className="inline-block bg-accent text-white px-6 py-3 rounded-lg font-medium hover:bg-opacity-90 transition-all"
            >
              Audit Another Product
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
