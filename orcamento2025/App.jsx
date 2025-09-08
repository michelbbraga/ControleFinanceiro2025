import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { TrendingUp, TrendingDown, DollarSign, PieChart, BarChart3 } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart as RechartsPieChart, Cell, Pie } from 'recharts'
import './App.css'

function App() {
  const API_BASE_URL = 'https://8xhpiqcezq7v.manus.space/api'
  
  // Estados para os dados
  const [acoes, setAcoes] = useState([])
  const [fiis, setFiis] = useState([])
  const [tesouroDireto, setTesouroDireto] = useState([])
  const [rendaFixa, setRendaFixa] = useState([])
  const [resumoGeral, setResumoGeral] = useState([])
  const [loading, setLoading] = useState(true)

  // Buscar dados da API
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        
        const [acoesRes, fiisRes, tesouroRes, rendaFixaRes, resumoRes] = await Promise.all([
          fetch(`${API_BASE_URL}/acoes`),
          fetch(`${API_BASE_URL}/fiis`),
          fetch(`${API_BASE_URL}/tesouro-direto`),
          fetch(`${API_BASE_URL}/renda-fixa`),
          fetch(`${API_BASE_URL}/resumo`)
        ])

        const acoesData = await acoesRes.json()
        const fiisData = await fiisRes.json()
        const tesouroData = await tesouroRes.json()
        const rendaFixaData = await rendaFixaRes.json()
        const resumoData = await resumoRes.json()

        setAcoes(acoesData)
        setFiis(fiisData)
        setTesouroDireto(tesouroData)
        setRendaFixa(rendaFixaData)
        setResumoGeral(resumoData)
      } catch (error) {
        console.error('Erro ao buscar dados:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // Função para calcular rentabilidade
  const calcularRentabilidade = (precoCompra, precoAtual, quantidade) => {
    const absoluta = (precoAtual - precoCompra) * quantidade
    const percentual = ((precoAtual - precoCompra) / precoCompra) * 100
    return { absoluta, percentual }
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
  }

  const formatPercentage = (value) => {
    return `${value.toFixed(2)}%`
  }

  const renderRentabilidadeBadge = (percentual) => {
    if (percentual > 0) {
      return (
        <Badge variant="default" className="bg-green-100 text-green-800 hover:bg-green-200">
          <TrendingUp className="w-3 h-3 mr-1" />
          {formatPercentage(percentual)}
        </Badge>
      )
    } else {
      return (
        <Badge variant="destructive" className="bg-red-100 text-red-800 hover:bg-red-200">
          <TrendingDown className="w-3 h-3 mr-1" />
          {formatPercentage(percentual)}
        </Badge>
      )
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Controle de Investimentos</h1>
          <p className="text-gray-600">Gerencie e acompanhe seus investimentos em tempo real</p>
        </header>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="text-lg">Carregando dados...</div>
          </div>
        ) : (

        <Tabs defaultValue="dashboard" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="acoes">Ações</TabsTrigger>
            <TabsTrigger value="fiis">FIIs</TabsTrigger>
            <TabsTrigger value="tesouro">Tesouro Direto</TabsTrigger>
            <TabsTrigger value="renda-fixa">Renda Fixa</TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {resumoGeral.map((item, index) => (
                <Card key={item.tipo}>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">{item.tipo}</CardTitle>
                    <DollarSign className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{formatCurrency(item.rentabilidadeAbsoluta)}</div>
                    <p className="text-xs text-muted-foreground">
                      {renderRentabilidadeBadge(item.rentabilidadePercentual)}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    Rentabilidade por Tipo de Ativo
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={resumoGeral}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="tipo" />
                      <YAxis />
                      <Tooltip formatter={(value) => formatPercentage(value)} />
                      <Bar dataKey="rentabilidadePercentual" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <PieChart className="h-5 w-5" />
                    Distribuição dos Investimentos
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <RechartsPieChart>
                      <Pie
                        data={resumoGeral}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ tipo, rentabilidadePercentual }) => `${tipo}: ${formatPercentage(rentabilidadePercentual)}`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="rentabilidadeAbsoluta"
                      >
                        {resumoGeral.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => formatCurrency(value)} />
                    </RechartsPieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="acoes">
            <Card>
              <CardHeader>
                <CardTitle>Ações</CardTitle>
                <CardDescription>Gerencie seus investimentos em ações</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Nome do Ativo</TableHead>
                      <TableHead>Empresa</TableHead>
                      <TableHead>Data da Compra</TableHead>
                      <TableHead>Quantidade</TableHead>
                      <TableHead>Preço de Compra</TableHead>
                      <TableHead>Preço Atual</TableHead>
                      <TableHead>Rentabilidade</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {acoes.map((acao, index) => {
                      const { absoluta, percentual } = calcularRentabilidade(acao.preco_compra, acao.preco_atual, acao.quantidade)
                      return (
                        <TableRow key={index}>
                          <TableCell className="font-medium">{acao.nome}</TableCell>
                          <TableCell>{acao.empresa}</TableCell>
                          <TableCell>{acao.data_compra}</TableCell>
                          <TableCell>{acao.quantidade}</TableCell>
                          <TableCell>{formatCurrency(acao.preco_compra)}</TableCell>
                          <TableCell>{formatCurrency(acao.preco_atual)}</TableCell>
                          <TableCell>
                            <div className="space-y-1">
                              <div>{formatCurrency(absoluta)}</div>
                              {renderRentabilidadeBadge(percentual)}
                            </div>
                          </TableCell>
                        </TableRow>
                      )
                    })}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="fiis">
            <Card>
              <CardHeader>
                <CardTitle>Fundos Imobiliários (FIIs)</CardTitle>
                <CardDescription>Gerencie seus investimentos em FIIs</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Nome do Ativo</TableHead>
                      <TableHead>Empresa</TableHead>
                      <TableHead>Data da Compra</TableHead>
                      <TableHead>Quantidade</TableHead>
                      <TableHead>Preço de Compra</TableHead>
                      <TableHead>Preço Atual</TableHead>
                      <TableHead>Rentabilidade</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {fiis.map((fii, index) => {
                      const { absoluta, percentual } = calcularRentabilidade(fii.preco_compra, fii.preco_atual, fii.quantidade)
                      return (
                        <TableRow key={index}>
                          <TableCell className="font-medium">{fii.nome}</TableCell>
                          <TableCell>{fii.empresa}</TableCell>
                          <TableCell>{fii.data_compra}</TableCell>
                          <TableCell>{fii.quantidade}</TableCell>
                          <TableCell>{formatCurrency(fii.preco_compra)}</TableCell>
                          <TableCell>{formatCurrency(fii.preco_atual)}</TableCell>
                          <TableCell>
                            <div className="space-y-1">
                              <div>{formatCurrency(absoluta)}</div>
                              {renderRentabilidadeBadge(percentual)}
                            </div>
                          </TableCell>
                        </TableRow>
                      )
                    })}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="tesouro">
            <Card>
              <CardHeader>
                <CardTitle>Tesouro Direto</CardTitle>
                <CardDescription>Gerencie seus investimentos no Tesouro Direto</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Nome do Ativo</TableHead>
                      <TableHead>Tipo</TableHead>
                      <TableHead>Vencimento</TableHead>
                      <TableHead>Rentabilidade Prevista</TableHead>
                      <TableHead>Preço de Compra</TableHead>
                      <TableHead>Preço Atual</TableHead>
                      <TableHead>Rentabilidade</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {tesouroDireto.map((titulo, index) => {
                      const { absoluta, percentual } = calcularRentabilidade(titulo.preco_compra, titulo.preco_atual, titulo.quantidade)
                      return (
                        <TableRow key={index}>
                          <TableCell className="font-medium">{titulo.nome}</TableCell>
                          <TableCell>{titulo.tipo}</TableCell>
                          <TableCell>{titulo.data_vencimento}</TableCell>
                          <TableCell>{titulo.rentabilidade_prevista}</TableCell>
                          <TableCell>{formatCurrency(titulo.preco_compra)}</TableCell>
                          <TableCell>{formatCurrency(titulo.preco_atual)}</TableCell>
                          <TableCell>
                            <div className="space-y-1">
                              <div>{formatCurrency(absoluta)}</div>
                              {renderRentabilidadeBadge(percentual)}
                            </div>
                          </TableCell>
                        </TableRow>
                      )
                    })}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="renda-fixa">
            <Card>
              <CardHeader>
                <CardTitle>Renda Fixa</CardTitle>
                <CardDescription>Gerencie seus investimentos em renda fixa</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Nome do Ativo</TableHead>
                      <TableHead>Instituição</TableHead>
                      <TableHead>Vencimento</TableHead>
                      <TableHead>Rentabilidade Prevista</TableHead>
                      <TableHead>Preço de Compra</TableHead>
                      <TableHead>Preço Atual</TableHead>
                      <TableHead>Rentabilidade</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {rendaFixa.map((investimento, index) => {
                      const { absoluta, percentual } = calcularRentabilidade(investimento.preco_compra, investimento.preco_atual, investimento.quantidade)
                      return (
                        <TableRow key={index}>
                          <TableCell className="font-medium">{investimento.nome}</TableCell>
                          <TableCell>{investimento.instituicao}</TableCell>
                          <TableCell>{investimento.data_vencimento}</TableCell>
                          <TableCell>{investimento.rentabilidade_prevista}</TableCell>
                          <TableCell>{formatCurrency(investimento.preco_compra)}</TableCell>
                          <TableCell>{formatCurrency(investimento.preco_atual)}</TableCell>
                          <TableCell>
                            <div className="space-y-1">
                              <div>{formatCurrency(absoluta)}</div>
                              {renderRentabilidadeBadge(percentual)}
                            </div>
                          </TableCell>
                        </TableRow>
                      )
                    })}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
        )}
      </div>
    </div>
  )
}

export default App

