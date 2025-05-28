# send-thankyou.ps1

# 1) Define your variables
$headers = @{ "Content-Type" = "application/json" }

$impactStatements = @(
  "Provided scholarships to 5 first‑generation college students"
  "Funded mentorship programs reaching over 200 under served youth"
)

$payload = @{
  donor_name          = "Dr. Jane Smith"
  donation_amount     = 150.00
  donation_date       = "2025-05-28"
  currency            = "USD"
  campaign            = "Annual Fund"
  organization_name   = "Helping Hands Foundation"
  contact_email       = "info@helpinghands.org"
  tone                = "warm"
  language            = "en"
  letter_length       = "standard"
  impact_statements   = $impactStatements
}

# 2) Convert to JSON (increase depth so arrays serialize properly)
$bodyJson = $payload | ConvertTo-Json -Depth 5

# 3) Send the request
$response = Invoke-RestMethod `
  -Uri "http://localhost:8000/generate" `
  -Method Post `
  -Headers $headers `
  -Body $bodyJson

# 4) Output the full letter
Write-Host "`n=== Generated Thank-You Letter ===`n"
Write-Host $response.letter
Write-Host "`n==================================`n"
