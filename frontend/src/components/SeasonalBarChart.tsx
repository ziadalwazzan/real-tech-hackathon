import * as React from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./SeasonalPriceCard";
import { Bar, BarChart, CartesianGrid, Cell, LabelList, ResponsiveContainer, XAxis, YAxis } from "recharts";

type MonthlyPoint = { month: string; value: number };

export function MonthlyBarChart({ data }: { data: MonthlyPoint[] }) {
  const dataValues = data.map((item) => item.value);
  const maxValue = Math.max(...dataValues);
  const minValue = Math.min(...dataValues);
  const range = maxValue - minValue;

  const shadedData = data.map((item) => {
    const ratio = range === 0 ? 0 : (item.value - minValue) / range;
    const lightness = 85 - ratio * 45;
    return {
      ...item,
      fill: `hsl(0 0% ${lightness.toFixed(0)}%)`,
    };
  });

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Seasonal Rental Prices</CardTitle>
        <CardDescription>Mean rental price changes across time</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={shadedData}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis dataKey="month" className="text-sm" />
            <YAxis className="text-sm" />
            <Bar dataKey="value" radius={[8, 8, 0, 0]}>
              {shadedData.map((entry) => (
                <Cell key={entry.month} fill={entry.fill} />
              ))}
              <LabelList
                dataKey="value"
                content={({ x, y, width, value }) => {
                  if (value !== maxValue && value !== minValue) return null;
                  if (typeof x !== "number" || typeof y !== "number" || typeof width !== "number") {
                    return null;
                  }
                  return (
                    <text
                      x={x + width / 2}
                      y={y - 6}
                      textAnchor="middle"
                      fill="#000"
                      fontSize={12}
                      fontWeight={600}
                    >
                      {value}
                    </text>
                  );
                }}
              />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
